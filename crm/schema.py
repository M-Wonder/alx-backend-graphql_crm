import graphene
from graphene_django import DjangoObjectType
from crm.models import Product  # Add this import

class ProductType(DjangoObjectType):
    class Meta:
        model = Product  # Use the actual Product model
        fields = ("id", "name", "stock", "price")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        try:
            # Find products with low stock
            low_stock_products = Product.objects.filter(stock__lt=10)
            
            # Update stock
            updated_products = []
            for product in low_stock_products:
                product.stock += 10
                product.save()
                updated_products.append(product)
            
            return UpdateLowStockProducts(
                success=True,
                message=f"Updated {len(updated_products)} products with low stock",
                updated_products=updated_products
            )
            
        except Exception as e:
            return UpdateLowStockProducts(
                success=False,
                message=f"Error updating low stock products: {str(e)}",
                updated_products=[]
            )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# Schema definition
schema = graphene.Schema(mutation=Mutation)
