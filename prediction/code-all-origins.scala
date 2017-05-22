sc.setLogLevel("OFF")

:paste


import org.apache.spark.rdd._
import scala.collection.JavaConverters._
import au.com.bytecode.opencsv.CSVReader

import java.io._
import org.joda.time._
import org.joda.time.format._

case class DelayRec(year: String,
                    month: String,
                    dayOfMonth: String,
                    dayOfWeek: String,
                    crsDepTime: String,
                    depDelay: String,
                    origin: String,
                    distance: String,
                    cancelled: String) {

    val holidays = List(
      //2001
      "01/01/2001", "01/15/2001", "02/19/2001", "05/28/2001", "07/04/2001", "09/03/2001",
      "10/08/2001", "11/12/2001", "11/22/2001", "12/25/2001",
      //2002
      "01/01/2002", "01/21/2002", "02/18/2002", "05/27/2002", "07/04/2002", "09/02/2002",
      "10/14/2002", "11/11/2002", "11/28/2002", "12/25/2002",
      //2003
      "01/01/2003", "01/20/2003", "02/17/2003", "05/26/2003", "07/04/2003", "09/01/2003",
      "10/13/2003", "11/11/2003", "11/27/2003", "12/25/2003",
      //2004
      "01/01/2004", "01/19/2004", "02/16/2004", "05/31/2004", "07/05/2004", "09/06/2004",
      "10/11/2004", "11/11/2004", "11/25/2004", "12/24/2004",
      //2005
      "12/31/2004", "01/17/2005", "02/21/2005", "05/30/2005", "07/04/2005", "09/05/2005",
      "10/10/2005", "11/11/2005", "11/24/2005", "12/26/2005",
      //2006
      "01/02/2006", "01/16/2006", "02/20/2006", "05/29/2006", "07/04/2006", "09/04/2006",
      "10/09/2006", "11/10/2006", "11/23/2006", "12/25/2006",
      //2007
      "01/01/2007", "01/15/2007", "02/19/2007", "05/28/2007", "07/04/2007", "09/03/2007",
      "10/08/2007" ,"11/11/2007", "11/22/2007", "12/25/2007",
      //2008
      "01/01/2008", "01/21/2008", "02/18/2008", "05/26/2008", "07/04/2008", "09/01/2008",
      "10/13/2008" ,"11/11/2008", "11/27/2008", "12/25/2008"
      )

    def gen_features: (String, Array[Double]) = {
      val values = Array(
        depDelay.toDouble,
        month.toDouble,
        dayOfMonth.toDouble,
        dayOfWeek.toDouble,
        get_hour(crsDepTime).toDouble,
        distance.toDouble,
        days_from_nearest_holiday(year.toInt, month.toInt, dayOfMonth.toInt)
      )
      new Tuple2(to_date(year.toInt, month.toInt, dayOfMonth.toInt), values)
    }

    def get_hour(depTime: String) : String = "%04d".format(depTime.toInt).take(2)
    def to_date(year: Int, month: Int, day: Int) = "%04d%02d%02d".format(year, month, day)

    def days_from_nearest_holiday(year:Int, month:Int, day:Int): Int = {
      val sampleDate = new DateTime(year, month, day, 0, 0)

      holidays.foldLeft(3000) { (r, c) =>
        val holiday = DateTimeFormat.forPattern("MM/dd/yyyy").parseDateTime(c)
        val distance = Math.abs(Days.daysBetween(holiday, sampleDate).getDays)
        math.min(r, distance)
      }
    }
  }

// function to do a preprocessing step for a given file
def prepFlightDelays(infile: String): RDD[DelayRec] = {
    val data = sc.textFile(infile)

    data.map { line =>
      val reader = new CSVReader(new StringReader(line))
      reader.readAll().asScala.toList.map(rec => DelayRec(rec(0),rec(1),rec(2),rec(3),rec(5),rec(15),rec(16),rec(18),rec(21)))
    }.map(list => list(0))
    .filter(rec => rec.year != "Year")
    .filter(rec => rec.cancelled == "0")
    //.filter(rec => rec.origin == "ORD")
}

val data = prepFlightDelays("/input/2001.csv").map(rec => rec.gen_features._2)
data.take(5).map(x => x mkString ",").foreach(println)

var i = 0;
for(i <- 2002 to 2008) {
  val data_i = prepFlightDelays("/input/" + i.toString + ".csv").map(rec => rec.gen_features._2)
  data_i.take(5).map(x => x mkString ",").foreach(println)
  data.union(data_i)
}

//val data_2007 = prepFlightDelays("/input/2007.csv").map(rec => rec.gen_features._2)
//val data_2008 = prepFlightDelays("/input/2008.csv").map(rec => rec.gen_features._2)
//data_2007.take(5).map(x => x mkString ",").foreach(println)
data.take(5).map(x => x mkString ",").foreach(println)

val Array(data_2007, data_2008) = data.randomSplit(Array(0.80, 0.20))

import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.feature.StandardScaler

def parseData(vals: Array[Double]): LabeledPoint = {
  LabeledPoint(if (vals(0)>=15) 1.0 else 0.0, Vectors.dense(vals.drop(1)))
}

// Prepare training set
val parsedTrainData = data_2007.map(parseData)
parsedTrainData.cache
val scaler = new StandardScaler(withMean = true, withStd = true).fit(parsedTrainData.map(x => x.features))
val scaledTrainData = parsedTrainData.map(x => LabeledPoint(x.label, scaler.transform(Vectors.dense(x.features.toArray))))
scaledTrainData.cache

// Prepare test/validation set
val parsedTestData = data_2008.map(parseData)
parsedTestData.cache
val scaledTestData = parsedTestData.map(x => LabeledPoint(x.label, scaler.transform(Vectors.dense(x.features.toArray))))
scaledTestData.cache

scaledTrainData.take(3).map(x => (x.label, x.features)).foreach(println)

// Function to compute evaluation metrics
def eval_metrics(labelsAndPreds: RDD[(Double, Double)]) : Tuple2[Array[Double], Array[Double]] = {
    val tp = labelsAndPreds.filter(r => r._1==1 && r._2==1).count.toDouble
    val tn = labelsAndPreds.filter(r => r._1==0 && r._2==0).count.toDouble
    val fp = labelsAndPreds.filter(r => r._1==1 && r._2==0).count.toDouble
    val fn = labelsAndPreds.filter(r => r._1==0 && r._2==1).count.toDouble

    val precision = tp / (tp+fp)
    val recall = tp / (tp+fn)
    val F_measure = 2*precision*recall / (precision+recall)
    val accuracy = (tp+tn) / (tp+tn+fp+fn)
    new Tuple2(Array(tp, tn, fp, fn), Array(precision, recall, F_measure, accuracy))
}

import org.apache.spark.mllib.classification.LogisticRegressionWithSGD

// Build the Logistic Regression model
val model_lr = LogisticRegressionWithSGD.train(scaledTrainData, numIterations=100)

// Predict
val labelsAndPreds_lr = scaledTestData.map { point =>
    val pred = model_lr.predict(point.features)
    (pred, point.label)
}

val m00_lr = eval_metrics(labelsAndPreds_lr)
val m0_lr = m00_lr._1
val m_lr = m00_lr._2
println("Logistic Regression: precision = %.2f, recall = %.2f, F1 = %.2f, accuracy = %.2f".format(m_lr(0), m_lr(1), m_lr(2), m_lr(3)))
println("tp = %.2f, tn = %.2f, fp = %.2f, fn = %.2f".format(m0_lr(0), m0_lr(1), m0_lr(2), m0_lr(3)))

import org.apache.spark.mllib.classification.SVMWithSGD

// Build the SVM model
val svmAlg = new SVMWithSGD()
svmAlg.optimizer.setNumIterations(100)
                .setRegParam(1.0)
                .setStepSize(1.0)
val model_svm = svmAlg.run(scaledTrainData)

// Predict
val labelsAndPreds_svm = scaledTestData.map { point =>
        val pred = model_svm.predict(point.features)
        (pred, point.label)
}

val m00_svm = eval_metrics(labelsAndPreds_svm)
val m0_svm = m00_svm._1
val m_svm = m00_svm._2
println("SVM: precision = %.2f, recall = %.2f, F1 = %.2f, accuracy = %.2f".format(m_svm(0), m_svm(1), m_svm(2), m_svm(3)))
println("tp = %.2f, tn = %.2f, fp = %.2f, fn = %.2f".format(m0_svm(0), m0_svm(1), m0_svm(2), m0_svm(3)))

import org.apache.spark.mllib.tree.DecisionTree

// Build the Decision Tree model
val numClasses = 2
val categoricalFeaturesInfo = Map[Int, Int]()
val impurity = "gini"
val maxDepth = 10
val maxBins = 100
val model_dt = DecisionTree.trainClassifier(parsedTrainData, numClasses, categoricalFeaturesInfo, impurity, maxDepth, maxBins)

// Predict
val labelsAndPreds_dt = parsedTestData.map { point =>
    val pred = model_dt.predict(point.features)
    (pred, point.label)
}

val m00_dt = eval_metrics(labelsAndPreds_dt)
val m0_dt = m00_dt._1
val m_dt = m00_dt._2
println("Decision Tree: precision = %.2f, recall = %.2f, F1 = %.2f, accuracy = %.2f".format(m_dt(0), m_dt(1), m_dt(2), m_dt(3)))
println("tp = %.2f, tn = %.2f, fp = %.2f, fn = %.2f".format(m0_dt(0), m0_dt(1), m0_dt(2), m0_dt(3)))