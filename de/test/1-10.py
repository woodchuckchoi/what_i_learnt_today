from pyspark.sql.functions import col, avg


superHeroDf = superHeroDf.distinct() # remove duplicates

superHeroDf.select('Race').distinct().show()
superHeroDf.sort(superHeroDf.Height.desc()).take(10) # Fin Fang Foom, whatever that is, is the biggest followed by Galactus?

superHeroDf.where((col('eye_color') == 'green') | (col('eye_color') == 'black')).take(5) # due to the parsing wrapper's design, the additional brackets are needed # A fella named 'Abomination' has green eyes?

superHeroDf.agg(avg('Height')).show()
