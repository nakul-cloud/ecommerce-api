# ==================================================
# Order Status Constants
# ==================================================

PENDING = "Pending"
CONFIRMED = "Confirmed"
PROCESSING = "Processing"
READY_FOR_SHIPMENT = "Ready For Shipment"
PICKED_UP = "Picked Up"
IN_TRANSIT = "In Transit"
OUT_FOR_DELIVERY = "Out For Delivery"
DELIVERED = "Delivered"
DELIVERY_FAILED = "Delivery Failed"
RETURNED = "Returned"
CANCELLED = "Cancelled"
REFUND_REQUESTED = "Refund Requested"
REFUND_APPROVED = "Refund Approved"
REFUND_REJECTED = "Refund Rejected"
REFUNDED = "Refunded"


# ==================================================
# Valid Status Transitions
# Each key maps to the list of statuses it may move INTO.
# Service layer enforces this before every UPDATE.
# ==================================================

VALID_TRANSITIONS: dict[str, list[str]] = {
    PENDING:            [CONFIRMED, CANCELLED],
    CONFIRMED:          [PROCESSING],
    PROCESSING:         [READY_FOR_SHIPMENT],
    READY_FOR_SHIPMENT: [PICKED_UP],
    PICKED_UP:          [IN_TRANSIT],
    IN_TRANSIT:         [OUT_FOR_DELIVERY],
    OUT_FOR_DELIVERY:   [DELIVERED, DELIVERY_FAILED],
    DELIVERY_FAILED:    [RETURNED],
    DELIVERED:          [REFUND_REQUESTED],
    REFUND_REQUESTED:   [REFUND_APPROVED, REFUND_REJECTED],
    REFUND_APPROVED:    [REFUNDED],
    REFUNDED:           [],
    REFUND_REJECTED:    [],
    CANCELLED:          [],
    RETURNED:           [],
}

# Flat list of every recognised status value
ORDER_STATUSES: list[str] = list(VALID_TRANSITIONS.keys())
