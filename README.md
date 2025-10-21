# Proyecto Final – Empleo Tech 2024: Oferta, coste de vida y skills

## 1. Objetivo del proyecto
En este proyecto quise analizar cómo se relacionan las **ofertas de empleo del sector tecnológico** con el **coste de vida** de los países y con las **habilidades más demandadas** durante 2024.  
La idea principal era entender si los países con más oportunidades también son los que tienen un coste de vida más alto, y ver qué tipo de puestos y skills aparecen con más frecuencia.

---

## 2. Datos y preparación
He usado dos fuentes principales: una con **ofertas de empleo tecnológicas** y otra con datos de **coste de vida por país**.  
Primero limpié los datos con **Python y Pandas**, uniendo ambas fuentes para crear un dataset final de unas **1,3 millones de filas**.

Los pasos más importantes fueron:
- Arreglar nombres de países para que coincidieran en ambas bases.  
- Crear una columna nueva con categorías simplificadas de área (`area_simple_dashboard` → datos_ia, desarrollo, cloud_devops, otros).  
- Quitar duplicados y registros incompletos.  
- Calcular varios porcentajes: % de ofertas remotas, % de ofertas con skills y % de ofertas de datos e IA.  
- Crear una tabla separada con las skills para usar como filtro en Power BI.

El archivo final que usé en el dashboard se llama **`empleo_coste_vida_2024.csv`** y está dentro de la carpeta `data/processed`.

---

## 3. Análisis de los datos
Antes de pasar al dashboard, hice un pequeño análisis para ver cómo se distribuían las ofertas.  
Vi que la mayoría se concentraban en **pocos países**, y que **Estados Unidos** tenía con mucha diferencia la mayor cantidad.  
También comprobé que el porcentaje de trabajo remoto era **muy bajo**, algo que me llamó la atención porque esperaba que fuera más alto.  
Las áreas de **Datos/IA** y **Cloud/DevOps** aparecen menos que las de desarrollo general, pero muestran un crecimiento importante.  
Además, observé que los países con **mayor coste de vida** suelen ser también los que más ofertas tienen.

---

## 4. Dashboard en Power BI
Para la parte visual utilicé **Power BI**. 
Los visuales que incluye el dashboard son:
- **Top 5 países con más ofertas.**  
- **Ofertas por área**, con la categoría “datos_ia” en verde.  
- **Relación entre ofertas y coste de vida por país** (gráfico de dispersión con eje logarítmico o las burbujas se me quedaban muy abajo).  
- **Skills más demandadas**, mostrando cuántas ofertas las mencionan.  
- **Proporción de remoto vs presencial** (donut).  
- **KPIs** con los principales indicadores: total de ofertas, % remoto, % con skills y % de datos IA.  
- **Slicers** para filtrar por país, área, tipo y skill.

Todos los visuales están conectados mediante una medida llamada **“Filtro skill (aplica visual)”**, que permite filtrar sin que afecte al resto de la página.  
Esto evita tener que usar filtros de página y mantiene el comportamiento uniforme.

---

## 5. Resultados y conclusiones
Después de analizar los datos y crear el dashboard, los resultados más destacados fueron:

1. **EE. UU.** concentra más del 85 % de todas las ofertas tecnológicas.  
2. El trabajo **remoto** apenas llega al 1 %, lo que indica que todavía la mayoría de empresas buscan empleados presenciales.  
3. Las áreas de **Datos e Inteligencia Artificial** tienen una presencia pequeña (alrededor del 3 %), pero son las que más crecen.  
4. Las **skills más pedidas** son **Excel, Python y SQL**, lo que demuestra que siguen siendo la base del trabajo con datos.  
5. Las **skills cloud** como AWS y Azure empiezan a aparecer más en combinación con IA.  
6. Los países con un **coste de vida más alto** suelen tener más volumen de ofertas, lo que puede reflejar mejores oportunidades laborales o salarios más competitivos.

---

## 6. Limitaciones
- Algunas fuentes no se actualizan al mismo ritmo, por lo que los datos no son totalmente homogéneos.  
- La columna de trabajo remoto puede no estar bien representada, ya que no todos los portales usan las mismas etiquetas.  
- No se incluyen datos de salarios, por lo que no se puede comparar el coste de vida con los ingresos reales.

---

## 7. Conclusión
Este proyecto me ha servido para poner en práctica todo lo aprendido durante el máster: desde la **limpieza y análisis de datos con Python**, hasta la **creación de dashboards en Power BI**.  
He podido comprobar lo importante que es preparar bien los datos antes de visualizarlos y cómo una buena organización facilita mucho el análisis.  
El resultado final es un dashboard que permite explorar de forma sencilla cómo está el mercado laboral tecnológico a nivel internacional y qué habilidades son las más valoradas.

Lo que mas me ha costado, además de lo obvio del aprendizaje, ha sido utilizar Power BI ya que he tenido que hacerlo en Virtual Box al tener Mac y ha sido una autentica pesadilla. Ha sido lento, se reiniciaba sin guardar, he tenido que empezar varias veces desde el principio, un horror, pero quería hacerlo en Power BI ya que los otros proyectos los hicimos en Excel y Google Sheet.

Por otro lado, el fichero era tan grande que me ha resultado una odisea abrirlo.

Pero me alegra haber podido "probar" la herramienta.
