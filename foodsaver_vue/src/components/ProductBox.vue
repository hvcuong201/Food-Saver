<template>
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
</template>

<script>
export default {
	name: 'ProductBox',
	props: {
		product: Object
	}
}
</script>

<style scoped>
.image {
	margin-top: -1.25rem;
	margin-left: -1.25rem;
	margin-right: -1.25rem;
}
</style>
