sc.setLogLevel("OFF")

:paste

import org.apache.spark.rdd._

import java.io._
import org.joda.time._
import org.joda.time.format._

import org.apache.spark.SparkContext._
import scala.collection.JavaConverters._
import au.com.bytecode.opencsv.CSVReader
import java.io._


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
    .filter(rec => rec.origin == "ORD")
}



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




// function to do a preprocessing step for a given file

def preprocess_spark(delay_file: String, weather_file: String): RDD[Array[Double]] = { 
  // Read wether data
  val delayRecs = prepFlightDelays(delay_file).map{ rec => 
        val features = rec.gen_features
        (features._1, features._2)
  }

  // Read weather data into RDDs
  val station_inx = 0
  val date_inx = 1
  val metric_inx = 2
  val value_inx = 3

  def filterMap(wdata:RDD[Array[String]], metric:String):RDD[(String,Double)] = {
    wdata.filter(vals => vals(metric_inx) == metric).map(vals => (vals(date_inx), vals(value_inx).toDouble))
  }

  val wdata = sc.textFile(weather_file).map(line => line.split(","))
                    .filter(vals => vals(station_inx) == "USW00094846")
  val w_tmin = filterMap(wdata,"TMIN")
  val w_tmax = filterMap(wdata,"TMAX")
  val w_prcp = filterMap(wdata,"PRCP")
  val w_snow = filterMap(wdata,"SNOW")
  val w_awnd = filterMap(wdata,"AWND")
  delayRecs.join(w_tmin).map(vals => (vals._1, vals._2._1 ++ Array(vals._2._2)))
           .join(w_tmax).map(vals => (vals._1, vals._2._1 ++ Array(vals._2._2)))
           .join(w_prcp).map(vals => (vals._1, vals._2._1 ++ Array(vals._2._2)))
           .join(w_snow).map(vals => (vals._1, vals._2._1 ++ Array(vals._2._2)))
           .join(w_awnd).map(vals => vals._2._1 ++ Array(vals._2._2))
}


// collecting all data
val data = preprocess_spark("/input/2001.csv", "/input/weather-2001.csv")
data.take(5).map(x => x mkString ",").foreach(println)
var i = 0;
for(i <- 2002 to 2008) {
  val data_i = preprocess_spark("/input/" + i.toString + ".csv", "/input/weather-" + i.toString + ".csv")
  data_i.take(5).map(x => x mkString ",").foreach(println)
  data.union(data_i)
}
data.cache

data.take(5).map(x => x mkString ",").foreach(println)

// splitting data into 80-20 train-test
val Array(data_2007, data_2008) = data.randomSplit(Array(0.80, 0.20))


// modeling with weather data

import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.feature.StandardScaler

def parseData(vals: Array[Double]): LabeledPoint = {
  LabeledPoint(if (vals(0)>=15) 1.0 else 0.0, Vectors.dense(vals.drop(1)))
}

// Prepare training set
val parsedTrainData = data_2007.map(parseData)
val scaler = new StandardScaler(withMean = true, withStd = true).fit(parsedTrainData.map(x => x.features))
val scaledTrainData = parsedTrainData.map(x => LabeledPoint(x.label, scaler.transform(Vectors.dense(x.features.toArray))))
parsedTrainData.cache
scaledTrainData.cache

// Prepare test/validation set
val parsedTestData = data_2008.map(parseData)
val scaledTestData = parsedTestData.map(x => LabeledPoint(x.label, scaler.transform(Vectors.dense(x.features.toArray))))
parsedTestData.cache
scaledTestData.cache

scaledTrainData.take(3).map(x => (x.label, x.features)).foreach(println)


// SVM

import org.apache.spark.mllib.classification.SVMWithSGD
import org.apache.spark.mllib.optimization.L1Updater

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
val model_dt = DecisionTree.trainClassifier(scaledTrainData, numClasses, categoricalFeaturesInfo, impurity, maxDepth, maxBins)

// Predict
val labelsAndPreds_dt = scaledTestData.map { point =>
    val pred = model_dt.predict(point.features)
    (pred, point.label)
}


val m00_svm = eval_metrics(labelsAndPreds_svm)
val m0_svm = m00_svm._1
val m_svm = m00_svm._2
println("SVM: precision = %.2f, recall = %.2f, F1 = %.2f, accuracy = %.2f".format(m_svm(0), m_svm(1), m_svm(2), m_svm(3)))
println("tp = %.2f, tn = %.2f, fp = %.2f, fn = %.2f".format(m0_svm(0), m0_svm(1), m0_svm(2), m0_svm(3)))