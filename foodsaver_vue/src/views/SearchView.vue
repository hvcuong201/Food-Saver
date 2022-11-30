<template>
	<div class="page-search">
		<div class="columns is-multiline">
			<div class="column is-12">
				<h1 class="title">Search</h1>

				<h2 class="is-size-5 has-text-grey">Search term: "{{ query }}"</h2>
			</div>
		</div>

		<div class="column is-3" v-for="product in products" v-bind:key="product.id" v-bind:product="product">
			<div class="box">
				<figure class="image mb-4 is-3by2">
					<img :src="product.get_thumbnail" />
				</figure>
				<h3 class="is-size-4">{{ product.name }} ({{ product.quantity }} {{ product.unit }}s)</h3>
				<p class="is-size-4 has-text-grey">${{ product.price }} per {{ product.unit }}</p>

				<RouterLink v-bind:to="product.get_absolute_url" class="button is-info mt-4">View Details</RouterLink>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'

export default {
	name: 'Search',
	data() {
		return {
			products: [],
			query: ''
		}
	},
	mounted() {
		document.title = 'Search | Food Saver'
		let uri = window.location.search.substring(1)
		let params = new URLSearchParams(uri)
		if (params.get('query')) {
			this.query = params.get('query')
			this.performSearch()
		}
	},
	methods: {
		async performSearch() {
			this.$store.commit('setIsLoading', true)
			await axios
				.post('/api/v1/products/search/', { query: this.query })
				.then((response) => {
					this.products = response.data
				})
				.catch((error) => {
					console.log(error)
				})
			this.$store.commit('setIsLoading', false)
		}
	}
}
</script>
