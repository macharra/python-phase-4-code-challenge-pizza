from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

# Define base
Base = declarative_base()

# revision identifiers, used by Alembic.
revision = 'e734db013d6f'
down_revision = '5c173aea779c'
branch_labels = None
depends_on = None

def upgrade():
    # Use batch mode for SQLite
    with op.batch_alter_table('pizzas') as batch_op:
        batch_op.alter_column('name', existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column('ingredients', existing_type=sa.VARCHAR(), nullable=False)

    with op.batch_alter_table('restaurants') as batch_op:
        batch_op.alter_column('name', existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column('address', existing_type=sa.VARCHAR(), nullable=False)

    # Add columns and constraints to the restaurant_pizzas table
    op.add_column('restaurant_pizzas', sa.Column('restaurant_id', sa.Integer(), nullable=False))
    op.add_column('restaurant_pizzas', sa.Column('pizza_id', sa.Integer(), nullable=False))

    op.create_foreign_key(
        'fk_restaurant_pizzas_restaurant_id_restaurants',
        'restaurant_pizzas', 'restaurants',
        ['restaurant_id'], ['id']
    )
    op.create_foreign_key(
        'fk_restaurant_pizzas_pizza_id_pizzas',
        'restaurant_pizzas', 'pizzas',
        ['pizza_id'], ['id']
    )

def downgrade():
    # Use batch mode for SQLite
    with op.batch_alter_table('restaurants') as batch_op:
        batch_op.alter_column('address', existing_type=sa.VARCHAR(), nullable=True)
        batch_op.alter_column('name', existing_type=sa.VARCHAR(), nullable=True)

    # Drop constraints and columns from restaurant_pizzas
    op.drop_constraint('fk_restaurant_pizzas_pizza_id_pizzas', 'restaurant_pizzas', type_='foreignkey')
    op.drop_constraint('fk_restaurant_pizzas_restaurant_id_restaurants', 'restaurant_pizzas', type_='foreignkey')
    op.drop_column('restaurant_pizzas', 'pizza_id')
    op.drop_column('restaurant_pizzas', 'restaurant_id')

    with op.batch_alter_table('pizzas') as batch_op:
        batch_op.alter_column('ingredients', existing_type=sa.VARCHAR(), nullable=True)
        batch_op.alter_
