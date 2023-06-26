from django.contrib import admin
from .models import Order, GroupPurchase, OrderItem, GroupPurchaseUser, OrderClaimHandle


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "is_deleted",
    )

    list_filter = ("user",)
    search_fields = ("user",)


@admin.register(GroupPurchase)
class GroupPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "display_users",
        "product_post",
        "required_participants",
        "end_time",
        "is_closed",
        "is_deleted",
    )

    def display_users(self, obj):
        return obj.users.count()

    display_users.short_description = "Users Count"

    list_filter = (
        "users",
        "product_post",
    )
    search_fields = (
        "users",
        "product_post",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "order",
        "pre_order_item",
        "scmNo",
        "status",
        "refund_amount",
        "is_deleted",
    )
    list_filter = (
        "order",
        "pre_order_item",
        "status",
    )
    search_fields = (
        "order",
        "pre_order_item",
        "scmNo",
        "status",
        "refund_amount",
    )


@admin.register(GroupPurchaseUser)
class GroupPurchaseUserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "group_purchase",
    )
    list_filter = (
        "user",
        "group_purchase",
    )
    search_fields = (
        "user",
        "group_purchase",
    )


@admin.register(OrderClaimHandle)
class OrderClaimHandleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "order_items_display",
        "claim_amount",
        "claim_reason",
        "claim_detail",
        "claim_answer_manager",
        "claim_answer",
        "claim_answer_date",
        "claim_account_name",
        "claim_account_bank",
        "claim_account_bank_code",
        "claim_date",
        "return_scmNo",
        "is_approved",
        "is_deleted",
    )
    list_filter = (
        "claim_reason",
        "claim_answer_manager",
        "claim_answer",
        "claim_answer_date",
    )
    search_fields = (
        "order_items",
        "claim_answer_manager",
        "claim_date",
    )

    def order_items_display(self, obj):
        return ", ".join([str(order_item) for order_item in obj.order_items.all()])

    order_items_display.short_description = "Order Items"


# @GroupPurchaseUser.register_lookup
# class GroupPurchaseUserLookup(Lookup):
#     lookup_name = "group_purchase_user"

#     # as_sql은 sql문을 만들어주는 함수
#     # lhs는 왼쪽항, rhs는 오른쪽항
#     # lhs_params는 왼쪽항의 파라미터, rhs_params는 오른쪽항의 파라미터
#     # lhs, rhs, params를 리턴해줘야함
#     #
#     def as_sql(self, compiler, connection):
#         lhs, lhs_params = self.process_lhs(compiler, connection)
#         rhs, rhs_params = self.process_rhs(compiler, connection)
#         params = lhs_params + rhs_params
#         return f"{lhs} = {rhs}", params

#     # process_rhs는 오른쪽항을 처리하는 함수
#     # compiler는 sql문을 만들어주는 객체, connection은 db에 연결하는 객체
#     # value는 오른쪽항의 값
#     # value가 GroupPurchaseUser인지 확인하고 맞으면 super().process_rhs를 리턴
#     # 아니면 오류를 발생시킴
#     def process_rhs(self, compiler, connection):
#         value = self.rhs
#         if isinstance(value, GroupPurchase):
#             return super().process_rhs(compiler, connection)
#         else:
#             raise ValueError("GroupPurchaseUserLookup only accepts GroupPurchase instance as value")

#     # get_prep_lookup은 오른쪽항의 값을 리턴해주는 함수

#     def get_prep_lookup(self):
#         return self.rhs.pk

#     # get_db_prep_lookup은 오른쪽항의 값을 db에 저장할 수 있는 형태로 바꿔주는 함수
#     # connection은 db에 연결하는 객체
#     # prepared는 db에 저장할 수 있는 형태로 바꿨는지 확인하는 변수
#     # value는 오른쪽항의 값
#     # value의 pk를 리턴

#     def get_db_prep_lookup(self, value, connection, prepared=False):
#         return value.pk


# @OrderItem.register_lookup
# class OrderItemLookup(Lookup):
#     lookup_name = "order_item"

#     def as_sql(self, compiler, connection):
#         lhs, lhs_params = self.process_lhs(compiler, connection)
#         rhs, rhs_params = self.process_rhs(compiler, connection)
#         params = lhs_params + rhs_params
#         return f"{lhs} = {rhs}", params

#     def process_rhs(self, compiler, connection):
#         value = self.rhs
#         if isinstance(value, Order):
#             return super().process_rhs(compiler, connection)
#         else:
#             raise ValueError("OrderItemLookup only accepts Order instance as value")

#     def get_prep_lookup(self):
#         return self.rhs.pk

#     def get_db_prep_lookup(self, value, connection, prepared=False):
#         return value.pk
