<template>
	<div class="home">
		<section class="hero is-medium is-info mb-6 has-bg-img">
			<div class="hero-body has-text-centered">
				<p class="title mb-6 is-1"><strong>Welcome to Food Saver</strong></p>
				<p class="subtitle is-3"><strong>Where No Food Left Behind</strong></p>
			</div>
		</section>
		<div class="columns is-multiline is-centered box">
			<div class="column is-10">
				<div class="columns is-multiline">
					<div class="column is-12">
						<h2 class="is-size-3 has-text-centered">New products</h2>
					</div>
					<div class="column is-3" v-for="product in latestProducts" v-bind:key="product.id">
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
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'

export default {
	name: 'HomeView',
	data() {
		return {
			latestProducts: []
		}
	},
	components: {},
	mounted() {
		this.getLatestProducts()

		document.title = 'Home | Food Saver'
	},
	methods: {
		async getLatestProducts() {
			this.$store.commit('setIsLoading', true)

			await axios
				.get('/api/v1/products/')
				.then((response) => {
					this.latestProducts = response.data
				})
				.catch((error) => {
					console.log(error)
				})

			this.$store.commit('setIsLoading', false)
		}
	}
}
</script>

<style scoped>
.image {
	margin-top: -1.25rem;
	margin-left: -1.25rem;
	margin-right: -1.25rem;
}

.box {
	height: 100%;
}
</style>

<style lang="scss">
.has-bg-img {
	background: url(https://as2.ftcdn.net/v2/jpg/05/47/63/53/1000_F_547635334_zmywmWyCIiPnNoKQDMglA3qxrBorW91O.jpg) center
		center;
	background-size: cover;
}
</style>
