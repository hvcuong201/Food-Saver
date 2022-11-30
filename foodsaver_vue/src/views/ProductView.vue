<template>
	<div class="page-product">
		<div class="columns is-multiline">
			<div class="column is-7">
				<figure class="image is-5by3">
					<img v-bind:src="product.get_image" />
				</figure>
			</div>

			<div class="column is-5">
				<h1 class="title">{{ product.name }}</h1>
				<h2 class="subtitle">{{ product.description }}</h2>
				<h2 class="subtitle">
					Sell by: <span class="has-text-info-dark">{{ product.get_vendor_name }}</span>
				</h2>
				<h2>Quantity: {{ product.quantity }} {{ product.unit }}s</h2>
				<h2><strong>Price: </strong>${{ product.price }} per {{ product.unit }}</h2>

				<div class="field has-addons mt-6">
					<div class="control">
						<input type="number" class="input" min="1" v-model="quantity" />
					</div>

					<div class="control">
						<a class="button is-info" @click="addToCart()">Add to cart</a>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
	name: 'Product',
	data() {
		return {
			product: {},
			quantity: 1
		}
	},
	mounted() {
		this.getProduct()
	},
	methods: {
		async getProduct() {
			this.$store.commit('setIsLoading', true)
			const category_slug = this.$route.params.category_slug
			const product_slug = this.$route.params.product_slug

			await axios
				.get(`/api/v1/products/${category_slug}/${product_slug}`)
				.then((response) => {
					this.product = response.data

					document.title = this.product.name + ' | Food Saver'
				})
				.catch((error) => {
					console.log(error)
				})

			this.$store.commit('setIsLoading', false)
		},
		addToCart() {
			if (isNaN(this.quantity) || this.quantity < 1) {
				this.quantity = 1
			}
			if (this.quantity > this.product.quantity) {
				toast({
					message: 'Exceeded the available quantity',
					type: 'is-danger',
					dismissible: true,
					pauseOnHover: true,
					duration: 1500,
					position: 'bottom-right'
				})
			} else {
				const item = {
					product: this.product,
					quantity: this.quantity
				}
				this.$store.commit('addToCart', item)
				toast({
					message: 'The Product was added to Cart',
					type: 'is-success',
					dismissible: true,
					pauseOnHover: true,
					duration: 1500,
					position: 'bottom-right'
				})
			}
		}
	}
}
</script>
