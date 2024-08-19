from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Configuración de SQLAlchemy y la conexión a MariaDB
DATABASE_URL = "mariadb+mariadbconnector://usuario:contraseña@localhost:3306/recetas_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Definición de los modelos
class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    ingredients = relationship('Ingredient', back_populates='recipe')
    steps = relationship('Step', back_populates='recipe')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient = Column(String(255), nullable=False)
    recipe = relationship('Recipe', back_populates='ingredients')

class Step(Base):
    __tablename__ = 'steps'
    
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    step = Column(String(255), nullable=False)
    recipe = relationship('Recipe', back_populates='steps')

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Función para agregar una nueva receta
def add_recipe():
    name = input("Nombre de la receta: ")
    recipe = Recipe(name=name)
    session.add(recipe)
    session.commit()
    
    add_ingredients(recipe.id)
    add_steps(recipe.id)

# Función para agregar ingredientes a una receta
def add_ingredients(recipe_id):
    print("Agregar ingredientes (dejar vacío para terminar):")
    while True:
        ingredient_name = input("Ingrediente: ")
        if ingredient_name == "":
            break
        ingredient = Ingredient(recipe_id=recipe_id, ingredient=ingredient_name)
        session.add(ingredient)
    session.commit()

# Función para agregar pasos a una receta
def add_steps(recipe_id):
    print("Agregar pasos (dejar vacío para terminar):")
    while True:
        step_description = input("Paso: ")
        if step_description == "":
            break
        step = Step(recipe_id=recipe_id, step=step_description)
        session.add(step)
    session.commit()

# Función para actualizar una receta existente
def update_recipe():
    list_recipes()
    recipe_id = int(input("ID de la receta a actualizar: "))
    option = input("Actualizar (1) Ingredientes o (2) Pasos: ")
    
    recipe = session.query(Recipe).get(recipe_id)
    if option == "1":
        session.query(Ingredient).filter_by(recipe_id=recipe_id).delete()
        add_ingredients(recipe_id)
    elif option == "2":
        session.query(Step).filter_by(recipe_id=recipe_id).delete()
        add_steps(recipe_id)
    session.commit()

# Función para eliminar una receta existente
def delete_recipe():
    list_recipes()
    recipe_id = int(input("ID de la receta a eliminar: "))
    
    session.query(Ingredient).filter_by(recipe_id=recipe_id).delete()
    session.query(Step).filter_by(recipe_id=recipe_id).delete()
    session.query(Recipe).filter_by(id=recipe_id).delete()
    session.commit()

# Función para ver todas las recetas
def list_recipes():
    recipes = session.query(Recipe).all()
    for recipe in recipes:
        print(f"{recipe.id}. {recipe.name}")

# Función para buscar los ingredientes y pasos de una receta
def search_recipe():
    list_recipes()
    recipe_id = int(input("ID de la receta a buscar: "))
    
    recipe = session.query(Recipe).get(recipe_id)
    
    print("\nIngredientes:")
    for ingredient in recipe.ingredients:
        print(f"- {ingredient.ingredient}")
    
    print("\nPasos:")
    for step in recipe.steps:
        print(f"- {step.step}")

# Función principal del menú
def menu():
    while True:
        print("\nLibro de Recetas")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")

        option = input("Seleccione una opción: ")

        if option == "1":
            add_recipe()
        elif option == "2":
            update_recipe()
        elif option == "3":
            delete_recipe()
        elif option == "4":
            list_recipes()
        elif option == "5":
            search_recipe()
        elif option == "6":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
