function fetchProduct(id) {
    fetch(`/api/product/${id}`)
    .then(res => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
    })
    .then(data => {
        alert(`Product: ${data.name}\nPrice: $${data.price}`);
    })
    .catch(error => {
        alert('Failed to fetch product details.');
        console.error('Fetch error:', error);
    });
}
