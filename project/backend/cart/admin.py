from django.contrib import admin
from cart.models import Cart, CartItem
from django.template.loader import get_template


@admin.action(description="Обновить общюю цену")
def ubdate_total_price(modeladmin, request, queryset):
    for item in queryset:
        item.update_total_price()


class CartItemAdminInline(admin.TabularInline):
    extra = 1
    model = CartItem
    fields = "product", "quantity"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemAdminInline,)
    fields = (
        "customer",
        "cart_items_inline",
        "total_price",
        "paid",
    )
    readonly_fields = ("total_price", "cart_items_inline")

    list_display = [
        "customer",
        "total_price",
        "paid",
    ]
    list_filter = ["paid"]
    search_fields = ["customer"]
    list_editable = ["paid"]
    actions = [ubdate_total_price]

    def cart_items_inline(self, *args, **kwargs):
        context = getattr(self.response, "context_data", None) or {}
        inline = context["inline_admin_formset"] = context["inline_admin_formsets"].pop(
            0
        )
        return get_template(inline.opts.template).render(context, self.request)

    def render_change_form(self, request, *args, **kwargs):
        self.request = request
        self.response = super().render_change_form(request, *args, **kwargs)
        return self.response
