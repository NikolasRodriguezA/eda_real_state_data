# eda_realstate.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (10, 6)

df = pd.read_csv("../data/Base.csv", sep=",", engine="python")
df.columns = df.columns.str.strip()
df = df.dropna(how="all")

for col in ["VALOR TOTAL", "VL. CUOTA INICIAL"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("[$,.]", "", regex=True)
        .str.strip()
        .replace("", None)
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\n📌 Información general:")
print(df.info())

print("\n📌 Estadísticas descriptivas:")
print(df.describe(include="all").T)

print("\n📌 Valores nulos:")
print(df.isnull().sum())


sns.histplot(df["VALOR TOTAL"].dropna(), bins=30, kde=True)
plt.title("Distribución del Valor Total de las Unidades")
plt.xlabel("Valor Total (COP)")
plt.ylabel("Frecuencia")
plt.show()


sns.countplot(data=df, x="TIPO", order=df["TIPO"].value_counts().index)
plt.title("Distribución por Tipo de Vivienda (VIS vs VIP)")
plt.show()


sns.countplot(data=df, x="ESTADO", order=df["ESTADO"].value_counts().index)
plt.title("Estados de las Unidades")
plt.show()


sns.boxplot(data=df, x="TIPO", y="VALOR TOTAL")
plt.title("Distribución de Precios por Tipo de Vivienda")
plt.show()


sns.boxplot(data=df, x="APLICA SUBSIDIO", y="VALOR TOTAL")
plt.title("Valor Total según Subsidio")
plt.show()


top_medios = df["MEDIO DE PUBLICIDAD"].value_counts().nlargest(10).index
sns.countplot(data=df[df["MEDIO DE PUBLICIDAD"].isin(top_medios)],
              x="MEDIO DE PUBLICIDAD")
plt.xticks(rotation=45)
plt.title("Top 10 Medios de Publicidad Usados")
plt.show()


ventas_anio = df.groupby("AÑO").size().reset_index(name="Ventas")
sns.barplot(data=ventas_anio, x="AÑO", y="Ventas")
plt.title("Ventas por Año")
plt.show()


ventas_mes = df.groupby("MES DE VENTA").size().reset_index(name="Ventas")
sns.barplot(data=ventas_mes, x="MES DE VENTA", y="Ventas",
            order=["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
                   "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"])
plt.title("Ventas por Mes")
plt.xticks(rotation=45)
plt.show()


num_cols = ["AREA CONST", "AREA PRIVADA", "VALOR TOTAL", "VL. CUOTA INICIAL"]
corr = df[num_cols].corr()

sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
plt.title("Matriz de Correlación")
plt.show()
