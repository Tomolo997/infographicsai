"""
Django management command to create credit packs in Stripe.

This command creates products and prices in Stripe for the following credit packs:
- 10 credits for $5
- 50 credits for $25
- 100 credits for $45
- 200 credits for $89

Usage:
    python manage.py create_credit_packs
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import stripe


class Command(BaseCommand):
    help = "Create credit pack products and prices in Stripe"

    def handle(self, *args, **options):
        # Set Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if not stripe.api_key:
            self.stdout.write(
                self.style.ERROR(
                    "STRIPE_SECRET_KEY is not set in settings. Please set it in your environment variables."
                )
            )
            return

        # Credit packs configuration
        credit_packs = [
            {
                "name": "10 Credits",
                "description": "10 credits to create amazing infographics",
                "credits": 10,
                "price": 500,  # $5.00 in cents
            },
            {
                "name": "50 Credits",
                "description": "50 credits to create amazing infographics",
                "credits": 50,
                "price": 2500,  # $25.00 in cents
            },
            {
                "name": "100 Credits",
                "description": "100 credits to create amazing infographics",
                "credits": 100,
                "price": 4500,  # $45.00 in cents
            },
            {
                "name": "200 Credits",
                "description": "200 credits to create amazing infographics",
                "credits": 200,
                "price": 8900,  # $89.00 in cents
            },
        ]

        self.stdout.write(
            self.style.SUCCESS("Creating credit pack products in Stripe...")
        )

        created_packs = []

        for pack in credit_packs:
            try:
                # Check if product already exists
                products = stripe.Product.list(limit=100)
                existing_product = None
                for product in products.data:
                    if product.name == pack["name"]:
                        existing_product = product
                        self.stdout.write(
                            self.style.WARNING(
                                f"Product '{pack['name']}' already exists with ID: {existing_product.id}"
                            )
                        )
                        break

                # Create product if it doesn't exist
                if not existing_product:
                    product = stripe.Product.create(
                        name=pack["name"],
                        description=pack["description"],
                        metadata={
                            "credits": pack["credits"],
                            "type": "credit_pack",
                        },
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Created product: {pack['name']} (ID: {product.id})"
                        )
                    )
                else:
                    product = existing_product

                # Check if price already exists for this product
                prices = stripe.Price.list(product=product.id, limit=100)
                existing_price = None
                for price in prices.data:
                    if (
                        price.unit_amount == pack["price"]
                        and price.currency == "usd"
                        and price.active
                    ):
                        existing_price = price
                        self.stdout.write(
                            self.style.WARNING(
                                f"Price for '{pack['name']}' already exists with ID: {existing_price.id}"
                            )
                        )
                        break

                # Create price if it doesn't exist
                if not existing_price:
                    price = stripe.Price.create(
                        product=product.id,
                        unit_amount=pack["price"],
                        currency="usd",
                        metadata={
                            "credits": pack["credits"],
                            "type": "credit_pack",
                        },
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Created price: ${pack['price']/100:.2f} (ID: {price.id})"
                        )
                    )
                    created_packs.append(
                        {
                            "name": pack["name"],
                            "credits": pack["credits"],
                            "price": pack["price"] / 100,
                            "product_id": product.id,
                            "price_id": price.id,
                        }
                    )
                else:
                    created_packs.append(
                        {
                            "name": pack["name"],
                            "credits": pack["credits"],
                            "price": pack["price"] / 100,
                            "product_id": product.id,
                            "price_id": existing_price.id,
                        }
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Using existing price: ${pack['price']/100:.2f} (ID: {existing_price.id})"
                        )
                    )

            except stripe.error.StripeError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Error creating {pack['name']}: {str(e)}"
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Unexpected error creating {pack['name']}: {str(e)}"
                    )
                )

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("Credit Packs Summary:"))
        self.stdout.write("=" * 60)

        for pack in created_packs:
            self.stdout.write(
                f"\n{pack['name']}:"
            )
            self.stdout.write(f"  Credits: {pack['credits']}")
            self.stdout.write(f"  Price: ${pack['price']:.2f}")
            self.stdout.write(f"  Product ID: {pack['product_id']}")
            self.stdout.write(f"  Price ID: {pack['price_id']}")

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(
            self.style.SUCCESS(
                "\n✓ Credit packs setup complete! Use the Price IDs in your application."
            )
        )
        self.stdout.write(
            self.style.WARNING(
                "\nNote: Store these Price IDs in your database or configuration for checkout."
            )
        )

