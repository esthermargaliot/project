
tools_weather = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

tools_catalog = [
    {
        "type": "function",
        "function": {
            "name": "add_product",
            "description": "Add a new product to the marketplace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the product."
                    },
                    "category_id": {
                        "type": "string",
                        "description": "The ID of the category to which the product belongs."
                    },
                    "price": {
                        "type": "number",
                        "description": "The price of the product."
                    },
                    "description": {
                        "type": "string",
                        "description": "A description of the product."
                    },
                    "stock": {
                        "type": "integer",
                        "description": "The number of items available in stock."
                    }
                },
                "required": ["name", "category_id", "price", "description", "stock"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_product",
            "description": "Update an existing product in the marketplace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product to update."
                    },
                    "name": {
                        "type": "string",
                        "description": "The new name of the product."
                    },
                    "category_id": {
                        "type": "string",
                        "description": "The new category ID for the product."
                    },
                    "price": {
                        "type": "number",
                        "description": "The new price of the product."
                    },
                    "description": {
                        "type": "string",
                        "description": "The new description of the product."
                    },
                    "stock": {
                        "type": "integer",
                        "description": "The new stock quantity for the product."
                    }
                },
                "required": ["product_id", "name", "category_id", "price", "description", "stock"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_product",
            "description": "Remove a product from the marketplace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product to remove."
                    }
                },
                "required": ["product_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_products_by_category",
            "description": "Retrieve products by category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category_id": {
                        "type": "string",
                        "description": "The ID of the category to retrieve products from."
                    }
                },
                "required": ["category_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_by_id",
            "description": "Retrieve a product by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product to retrieve."
                    }
                },
                "required": ["product_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_products_by_name",
            "description": "Search for products by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the product to search for."
                    }
                },
                "required": ["name"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_category",
            "description": "Add a new category to the marketplace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category_name": {
                        "type": "string",
                        "description": "The name of the category to add."
                    }
                },
                "required": ["category_name"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]