<template>
	<tr>
		<td>
			<router-link :to="item.product.get_absolute_url">{{ item.product.name }}</router-link>
		</td>
		<td>{{ item.product.get_vendor_name }}</td>
		<td>${{ item.product.price }}</td>
		<td>
			{{ item.quantity }}
			<a class="button is-small is-success is-outlined is-rounded" @click="incrementQuantity(item)"
				><i class="fa fa-plus"></i
			></a>
			<a class="button is-small is-danger is-outlined is-rounded" @click="decrementQuantity(item)"
				><i class="fa fa-minus"></i
			></a>
		</td>
		<td>${{ getItemTotal(item).toFixed(2) }}</td>
		<td><button class="delete" @click="removeFromCart(item)"></button></td>
	</tr>
</template>

<script>
import { toast } from 'bulma-toast'

export default {
	name: 'CartItem',
	props: {
		initialItem: Object
	},
	data() {
		return {
			item: this.initialItem
		}
	},
	methods: {
		getItemTotal(item) {
			return item.quantity * item.product.price
		},
		decrementQuantity(item) {
			item.quantity -= 1
			if (item.quantity === 0) {
				this.$emit('removeFromCart', item)
			}
			this.updateCart()
		},
		incrementQuantity(item) {
			item.quantity += 1
			if (item.quantity > item.product.quantity) {
				item.quantity = item.product.quantity

				toast({
					message: 'Exceeded the available quantity',
					type: 'is-danger',
					dismissible: true,
					pauseOnHover: true,
					duration: 1500,
					position: 'bottom-right'
				})
			}
			this.updateCart()
		},
		updateCart() {
			localStorage.setItem('cart', JSON.stringify(this.$store.state.cart))
		},
		removeFromCart(item) {
			this.$emit('removeFromCart', item)
			this.updateCart()
		}
	}
}
</script>
