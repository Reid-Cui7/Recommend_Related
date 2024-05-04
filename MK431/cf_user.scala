import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.catalyst.ScalaReflection
import org.apache.spark.sql.types.StructType
import org.apache.spark.sql.functions._
import spark.implicits._



object Test {

    case class UserItem(userId: String, itemId: String, score: Double)

    def main(args: Array[String]): Unit = {
        val spark = SparkSession.builder()
            .master("local")
            .getOrCreate()

        val df = spark.read.format("csv")
            .option("header", true)
            .option("delimiter", ",")
            .option("inferschema", true)
            .schema(ScalaReflection.schemaFor[UserItem].dataType.asInstanceOf[StructType])
            .load("zcmj/test/cf_user_based.csv")

        df.show(false)
        df.printSchema()

        // 分母 
        val dfScoreMod = df.rdd.map(x => (x(0).toString, x(2).toString))
            .groupByKey()
            .mapValues(score => math.sqrt(
                score.toArray.map(
                    itemScore => math.pow(itemScore.toDouble, 2)
                ).reduce(_+_)
            ))
            .toDF("userId", "mod")

        dfScoreMod.show(false)

        // 分子
        val _dfTmp = df.select(
            col("userId").as("_userId"),
            col("itemId"),
            col("score").as("_score")
        )

        // 引起shuffle
        val _df = df.join(_dfTmp, df("itemId") === _dfTmp("itemId"))
            .where(
                df("userId") =!= _dfTmp("_userId")
            )
            .select(
                df("itemId"),
                df("userId"),
                _dfTmp("_userId"),
                df("score"),
                _dfTmp("_score")
            )
        
        _df.show(false)

        // 两两相良的维度乘积并加总
        val df_mol = _df.select(
            col("userId"),
            col("_userId"),
            (col("score") * col("_score")).as("score_mol") // 用户a, b对同一物品打分的乘积
        ).groupBy(col("userId"), col("_userId"))
        .agg(sum("score_mol"))
        .withColumnRenamed("sum(score_mol)", "mol")

        df_mol.show(false)

        val _dfScoreMod = dfScoreMod.select(
            col("userId").as("_userId"),
            col("mod").as("_mod")
        )

        // 这里也会引起shuffle
        val sim = df_mol.join(dfScoreMod, df_mol("userId") === dfScoreMod("userId"))
            .join(_dfScoreMod, df_mol("_userId") === _dfScoreMod("_userId"))
            .select(
                df_mol("userId"),
                df_mol("_userId"),
                df_mol("mol"),
                dfScoreMod("mod"),
                _dfScoreMod("_mod")
            )

        sim.show(false)

        val cos_sim = sim.select(
            col("userId"),
            col("_userId"),
            (col("mol") / (col("mod") * col("_mod"))).as("cos_sim")
        )

        cos_sim.show(false)

        val topN = cos_sim.rdd.map(x => (
            (x(0).toString, (x(1).toString, x(2).toString)) // (uid1, (uid2, cos_sim))
        )).groupByKey()
          .mapValues(_.toArray.sortWith((x, y) => x._2 > y._2))
          .flatMapValues(x => x)
          .toDF("userId", "sim_sort")
          .select(
            col("userId"),
            col("sim_sort._1").as("_userId"),
            col("sim_sort._2").as("cos_sim")
        ).where(col("userId") === "1")

        topN.show(false)

    }
}



