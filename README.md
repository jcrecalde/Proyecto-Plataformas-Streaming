 
# Data Engineering
 
Mi nombre es Juan Cruz Recalde, estoy estudiando en Henry y en este momento me encuentro en los Labs. En este proyecto, presentaré una solución que nos sitúa en el rol de un Data Engineer con conocimientos en Machin Learning. El objetivo del proyecto es unir y transformar cuatro conjuntos de datos en formato CSV de las principales plataformas de streaming como Amazon,Disney,Hulu y Netflix, Asi como ocho conjuntos de datos adicionales que contiene la clasificacion de los usuarios. Para lograrlo realice un proceso ETL y un analisis exploratorio de datos(EDA), sobre cada conjunto de datos. Una vez que tengo unidos los datos, construyo la API y se entrena un modelo de ML de recomendacion.  
 
# Objetivos: 
 
El objetivo principal de este proyecto es realizar un trabajo de ETL sobre los conjuntos de datos proporcionados y luego desarrollar una API con diferentes endpoints que permitan el consumo de información. 
 
La API constará de 6 funciones diseñadas para brindar diferentes análisis y perspectivas sobre los datos disponibles. La primera función, llamada `get_max_duration`, mostrará la pelicula con mayor duración según año,plataforma y tipo de duracion. La segunda función, llamada `get_score_count`, mostrará la cantidad de películas segun la plataforma con un puntaje mayor a un determinado año. La tercera funcion, `get_count_platform`, mostrará la cantidad de películas según plataforma. La cuarta función, llamada `get_actor`, mostrará el actor que mas se repite segun la plataforma y el año. La quinta función, `prod_per_country`, mostrará la cantidad de contenidos/productos todo lo que se encuentra disponible en streaming que se publicaron por país y años. Por ultimo realice la ultima función que se llama `get_contents`, que muestra la cantidad total de contenidos/producots según el rating de audiencia dado.

# Contenido del repositorio 
 
En este repositorio se encuentran diferentes elementos que conforman el proyecto, tales como: 
  
-Un notebook llamado ETL.ipynb, donde se presenta el código utilizado para realizar el proceso de Extracción, Transformación y Carga de los datos. Este notebook está comentado para explicar paso a paso las decisiones tomadas durante el proyecto.
 
- Otro notebook llamado EDA.ipynb, donde se lleva a cabo un pequeño análisis exploratorio de los datos obtenidos luego del ETL. Se verifica la presencia de valores atípicos, registros erróneos y anómalos. 
 
- El archivo main.py, que contiene todas las funciones necesarias para la API y está listo para el despliegue. 
 
- Un notebook llamado ML.ipynb, donde se realiza un ETL y EDA adicional para configurar un sistema de recomendación de manera óptima. 
 
- Dos archivos CSV llamados plataformas.csv y ML.csv, que contienen los datasets trabajados o finales utilizados para la implementación de las funciones de la API. 
 
- Un notebook llamado funciones.ipynb, que es una copia de las funciones de la API utilizadas para realizar pruebas de manera más rápida. Ya que utilizo Jupyter !   
 
- Los datasets originales utilizados en el proyecto se encuentran en el siguiente drive: https://drive.google.com/drive/u/0/folders/1T02IMQyVbaf2iPDh_gmwh885s1RNNgIQ. 
 
- El archivo requirements.txt, que contiene las librerías utilizadas para el despliegue. Esto es muy necesario para que en el render funcione ! 
 
- El archivo .gitignore, que se creó para evitar que se carguen todos los archivos en GitHub y solo se carguen los que se desean. 

# Herramientas Utilizadas 
 
- VSC 
- Python 
- Render 
- FastApi 
 
# Librerías 
 
- Pandas 
- Matplotlib 
- Seaborn  
- Uvicorn 
- scikit-learn (TfidfVectorizer - cosine_similarity) 
 
# Links:
Video Explicativo de la API:https://www.youtube.com/watch?v=XOceBlqJRco

Deploy de la API en Render:https://pi-pkk4.onrender.com/docs

 

