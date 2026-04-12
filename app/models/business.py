from pydantic import BaseModel
from typing import Optional


class ColumnDescription(BaseModel):
    name: str
    type: str
    description: str
    is_primary_key: bool = False
    is_foreign_key: bool = False


class TableDescription(BaseModel):
    name: str
    description: str
    columns: list[ColumnDescription]


class RestaurantContext(BaseModel):
    business_id: str = "restaurant_001"
    name: str = "Restaurante Demo"
    description: str = (
        "Sistema de gestión de restaurantes (RMS). El restaurante tiene áreas de "
        "preparación (Cocina Principal, Bar, Postres), ofrece productos de menú con "
        "opciones personalizables, y gestiona pedidos de clientes en mesas. También "
        "maneja inventario de insumos y proceso de compras a proveedores."
    )
    db_type: str = "mysql"

    tables: list[TableDescription] = [
        TableDescription(
            name="areas",
            description="Áreas físicas o lógicas del restaurante donde se preparan los productos.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name",
                    type="VARCHAR(255)",
                    description="Nombre del área (ej: 'Cocina Principal', 'Bar', 'Postres')",
                ),
                ColumnDescription(
                    name="type",
                    type="VARCHAR(50)",
                    description="Tipo: KITCHEN, BAR, DESSERT",
                ),
                ColumnDescription(
                    name="enabled", type="BOOLEAN", description="Si el área está activa"
                ),
            ],
        ),
        TableDescription(
            name="users",
            description="Usuarios del sistema (meseros, admins, etc.)",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="document",
                    type="VARCHAR(255)",
                    description="Documento de identidad (único)",
                ),
                ColumnDescription(
                    name="name", type="VARCHAR(255)", description="Nombre completo"
                ),
                ColumnDescription(
                    name="email",
                    type="VARCHAR(255)",
                    description="Correo electrónico (único)",
                ),
                ColumnDescription(
                    name="address", type="VARCHAR(255)", description="Dirección"
                ),
                ColumnDescription(
                    name="phone", type="VARCHAR(50)", description="Teléfono"
                ),
                ColumnDescription(
                    name="role",
                    type="VARCHAR(50)",
                    description="Rol: ADMIN, WAITER, MANAGER, etc.",
                ),
            ],
        ),
        TableDescription(
            name="categories",
            description="Categorías de productos del menú.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name",
                    type="VARCHAR(255)",
                    description="Nombre (ej: 'Bebidas', 'Platos Fuertes', 'Postres')",
                ),
                ColumnDescription(
                    name="description", type="VARCHAR(500)", description="Descripción"
                ),
                ColumnDescription(
                    name="enabled",
                    type="BOOLEAN",
                    description="Si la categoría está activa",
                ),
            ],
        ),
        TableDescription(
            name="tables",
            description="Mesas del restaurante.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="table_number",
                    type="INTEGER",
                    description="Número de mesa (único)",
                ),
                ColumnDescription(
                    name="capacity", type="INTEGER", description="Capacidad de personas"
                ),
                ColumnDescription(
                    name="status",
                    type="VARCHAR(50)",
                    description="Estado: AVAILABLE, OCCUPIED, RESERVED",
                ),
            ],
        ),
        TableDescription(
            name="products",
            description="Productos del menú.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name", type="VARCHAR(255)", description="Nombre del producto"
                ),
                ColumnDescription(
                    name="base_price", type="DECIMAL(10,2)", description="Precio base"
                ),
                ColumnDescription(
                    name="has_options",
                    type="BOOLEAN",
                    description="Si tiene opciones personalizables (cocción, tamaño, etc.)",
                ),
                ColumnDescription(
                    name="active", type="BOOLEAN", description="Si está activo/en venta"
                ),
                ColumnDescription(
                    name="category_id",
                    type="BIGINT",
                    description="FK a categories",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="area_id",
                    type="BIGINT",
                    description="FK a areas (área principal de preparación)",
                    is_foreign_key=True,
                ),
            ],
        ),
        TableDescription(
            name="product_options",
            description="Opciones personalizables de productos (ej: niveles de cocción, tamaños).",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name",
                    type="VARCHAR(255)",
                    description="Nombre de la opción (ej: 'Rare', 'Medium', 'Personal (8\")')",
                ),
                ColumnDescription(
                    name="option_category_id",
                    type="BIGINT",
                    description="FK a option_categories",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="product_id",
                    type="BIGINT",
                    description="FK a products",
                    is_foreign_key=True,
                ),
            ],
        ),
        TableDescription(
            name="option_categories",
            description="Categorías de opciones (ej: 'Tipo de Cocción', 'Tamaño').",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name",
                    type="VARCHAR(255)",
                    description="Nombre de la categoría",
                ),
                ColumnDescription(
                    name="description", type="VARCHAR(500)", description="Descripción"
                ),
            ],
        ),
        TableDescription(
            name="orders",
            description="Pedidos de clientes.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="date", type="TIMESTAMP", description="Fecha y hora del pedido"
                ),
                ColumnDescription(
                    name="status",
                    type="VARCHAR(50)",
                    description="Estado: QUEUE, PREPARING, READY, DELIVERED, CANCELLED",
                ),
                ColumnDescription(
                    name="table_id",
                    type="BIGINT",
                    description="FK a tables (mesa del pedido)",
                    is_foreign_key=True,
                ),
            ],
        ),
        TableDescription(
            name="order_details",
            description="Detalles/items de cada pedido.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="order_id",
                    type="BIGINT",
                    description="FK a orders",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="product_id",
                    type="BIGINT",
                    description="FK a products",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="unit_price",
                    type="DECIMAL(10,2)",
                    description="Precio unitario al momento del pedido",
                ),
                ColumnDescription(
                    name="instructions",
                    type="VARCHAR(500)",
                    description="Instrucciones especiales del cliente",
                ),
            ],
        ),
        TableDescription(
            name="order_detail_options",
            description="Opciones seleccionadas para cada item del pedido.",
            columns=[
                ColumnDescription(
                    name="order_detail_id",
                    type="BIGINT",
                    description="FK a order_details",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="option_id",
                    type="BIGINT",
                    description="FK a product_options",
                    is_foreign_key=True,
                ),
            ],
        ),
        TableDescription(
            name="order_preparation_areas",
            description="Relación many-to-many entre pedidos y áreas de preparación.",
            columns=[
                ColumnDescription(
                    name="order_id",
                    type="BIGINT",
                    description="FK a orders",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="area_id",
                    type="BIGINT",
                    description="FK a areas",
                    is_foreign_key=True,
                ),
            ],
        ),
        TableDescription(
            name="supply_categories",
            description="Categorías de insumos (ej: 'Proteínas', 'Vegetales', 'Lácteos').",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name", type="VARCHAR(255)", description="Nombre (único)"
                ),
            ],
        ),
        TableDescription(
            name="units_of_measure",
            description="Unidades de medida estándar.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name",
                    type="VARCHAR(100)",
                    description="Nombre (ej: 'Gramos', 'Mililitros', 'Unidades')",
                ),
                ColumnDescription(
                    name="abbreviation",
                    type="VARCHAR(20)",
                    description="Abreviatura (ej: 'g', 'ml', 'u')",
                ),
            ],
        ),
        TableDescription(
            name="supplies",
            description="Insumos base del inventario.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name",
                    type="VARCHAR(255)",
                    description="Nombre (ej: 'Carne de Res', 'Arroz')",
                ),
                ColumnDescription(
                    name="supply_category_id",
                    type="BIGINT",
                    description="FK a supply_categories",
                    is_foreign_key=True,
                ),
            ],
        ),
        TableDescription(
            name="supply_variants",
            description="Presentaciones físicas de un insumo.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="supply_id",
                    type="BIGINT",
                    description="FK a supplies",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="unit_id",
                    type="BIGINT",
                    description="FK a units_of_measure",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="quantity",
                    type="DECIMAL(10,3)",
                    description="Cantidad (ej: 250)",
                ),
            ],
        ),
        TableDescription(
            name="storage_locations",
            description="Ubicaciones físicas de almacenamiento (ej: 'Bodega Principal', 'Cocina').",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name", type="VARCHAR(255)", description="Nombre (único)"
                ),
            ],
        ),
        TableDescription(
            name="inventory_stock",
            description="Stock actual de cada variante de insumo en cada ubicación.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="supply_variant_id",
                    type="BIGINT",
                    description="FK a supply_variants",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="storage_location_id",
                    type="BIGINT",
                    description="FK a storage_locations",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="current_quantity",
                    type="DECIMAL(10,3)",
                    description="Cantidad actual",
                ),
            ],
        ),
        TableDescription(
            name="product_recipes",
            description="Recetas de productos: qué insumos se necesitan.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="product_id",
                    type="BIGINT",
                    description="FK a products",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="supply_variant_id",
                    type="BIGINT",
                    description="FK a supply_variants",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="required_quantity",
                    type="DECIMAL(10,3)",
                    description="Cantidad requerida",
                ),
            ],
        ),
        TableDescription(
            name="option_recipes",
            description="Recetas de opciones de productos.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="option_id",
                    type="BIGINT",
                    description="FK a product_options",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="supply_variant_id",
                    type="BIGINT",
                    description="FK a supply_variants",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="required_quantity",
                    type="DECIMAL(10,3)",
                    description="Cantidad requerida",
                ),
            ],
        ),
        TableDescription(
            name="inventory_movements",
            description="Historial de movimientos de inventario.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="supply_variant_id",
                    type="BIGINT",
                    description="FK a supply_variants",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="from_storage_location_id",
                    type="BIGINT",
                    description="FK a storage_locations (origen, null si es ingreso)",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="to_storage_location_id",
                    type="BIGINT",
                    description="FK a storage_locations (destino, null si es consumo)",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="quantity", type="DECIMAL(10,3)", description="Cantidad movida"
                ),
                ColumnDescription(
                    name="movement_type",
                    type="VARCHAR(50)",
                    description="Tipo: TRANSFER, DEDUCTION, ENTRY",
                ),
                ColumnDescription(
                    name="reference_order_id",
                    type="BIGINT",
                    description="FK a orders (referencia al pedido relacionado)",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="reference_purchase_order_id",
                    type="BIGINT",
                    description="FK a purchase_orders (referencia a orden de compra)",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="created_at",
                    type="TIMESTAMP",
                    description="Fecha del movimiento",
                ),
            ],
        ),
        TableDescription(
            name="suppliers",
            description="Proveedores/distribuidores.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="name", type="VARCHAR(255)", description="Nombre del proveedor"
                ),
                ColumnDescription(
                    name="contact",
                    type="VARCHAR(255)",
                    description="Información de contacto",
                ),
                ColumnDescription(
                    name="active", type="BOOLEAN", description="Si está activo"
                ),
            ],
        ),
        TableDescription(
            name="purchase_orders",
            description="Órdenes de compra (cabecera).",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="supplier_id",
                    type="BIGINT",
                    description="FK a suppliers",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="registered_by",
                    type="BIGINT",
                    description="FK a users (usuario que registró)",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="purchased_at", type="TIMESTAMP", description="Fecha de compra"
                ),
                ColumnDescription(
                    name="total_amount", type="DECIMAL(12,2)", description="Monto total"
                ),
                ColumnDescription(
                    name="notes", type="VARCHAR(500)", description="Notas"
                ),
                ColumnDescription(
                    name="created_at", type="TIMESTAMP", description="Fecha de creación"
                ),
            ],
        ),
        TableDescription(
            name="purchase_order_items",
            description="Ítems de las órdenes de compra.",
            columns=[
                ColumnDescription(
                    name="id",
                    type="BIGINT",
                    description="Identificador único",
                    is_primary_key=True,
                ),
                ColumnDescription(
                    name="purchase_order_id",
                    type="BIGINT",
                    description="FK a purchase_orders",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="supply_variant_id",
                    type="BIGINT",
                    description="FK a supply_variants",
                    is_foreign_key=True,
                ),
                ColumnDescription(
                    name="quantity_ordered",
                    type="DECIMAL(10,3)",
                    description="Cantidad ordenada",
                ),
                ColumnDescription(
                    name="quantity_received",
                    type="DECIMAL(10,3)",
                    description="Cantidad recibida",
                ),
                ColumnDescription(
                    name="unit_price",
                    type="DECIMAL(10,2)",
                    description="Precio unitario",
                ),
            ],
        ),
    ]

    restricted_tables: list[str] = [
        "users",
        "refresh_tokens",
        "two_factor_codes",
        "devices",
        "password_reset_tokens",
        "user_assigned_areas",
    ]

    restricted_fields: dict[str, list[str]] = {
        "users": ["password", "address", "phone"],
    }

    business_rules: str = """
REGLAS DE NEGOCIO:
- Los clientes inactivos son aquellos sin pedidos entregados en los últimos 6 meses.
- Un pedido pasa por los estados: QUEUE → PREPARING → READY → DELIVERED (o CANCELLED).
- Los insumos con stock menor al 20% del stock mínimo deben mostrarse como "en alerta".
- Las órdenes de compra se consideran completadas cuando quantity_ordered == quantity_received.
- Los productos con has_options=true tienen opciones personalizables (ej: tipo de cocción, tamaño).
- Cada producto pertenece a un área de preparación principal (area_id).
- Los movimientos de inventario pueden ser: ENTRY (ingreso), DEDUCTION (consumo), TRANSFER (traslado).
- Un pedido puede involucrar múltiples áreas de preparación (order_preparation_areas).
"""

    example_queries: list[str] = [
        "SELECT DATE(o.date) as dia, COUNT(*) as pedidos, SUM(od.unit_price) as total "
        "FROM orders o "
        "JOIN order_details od ON o.id = od.order_id "
        "WHERE o.status = 'DELIVERED' "
        "AND o.date >= DATE_SUB(NOW(), INTERVAL 7 DAY) "
        "GROUP BY DATE(o.date) "
        "ORDER BY dia;",
        "SELECT p.name, COUNT(od.id) as veces_vendido, SUM(od.unit_price) as revenue "
        "FROM order_details od "
        "JOIN products p ON od.product_id = p.id "
        "JOIN orders o ON od.order_id = o.id "
        "WHERE o.status = 'DELIVERED' "
        "GROUP BY p.id, p.name "
        "ORDER BY revenue DESC "
        "LIMIT 10;",
        "SELECT s.name, sv.quantity, u.name as unit, sl.name as location, ins.current_quantity "
        "FROM inventory_stock ins "
        "JOIN supply_variants sv ON ins.supply_variant_id = sv.id "
        "JOIN supplies s ON sv.supply_id = s.id "
        "JOIN units_of_measure u ON sv.unit_id = u.id "
        "JOIN storage_locations sl ON ins.storage_location_id = sl.id;",
        "SELECT t.table_number, o.status, COUNT(od.id) as items "
        "FROM orders o "
        "LEFT JOIN tables t ON o.table_id = t.id "
        "LEFT JOIN order_details od ON o.id = od.order_id "
        "GROUP BY t.table_number, o.status;",
    ]


restaurant_context = RestaurantContext()
