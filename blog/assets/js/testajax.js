function like(slug, id) {
  var element = document.getElementById('like');
  var count = document.getElementById('count');
  $.get(`/articles/like/${slug}/${id}`).then(response => {
    if(response['response'] == 'liked') {
      element.className = "fa fa-heart";
      count.innerText = Number(count.innerText) + 1
    }
    else {
      element.className = "fa fa-heart-o";
      count.innerText = Number(count.innerText) - 1
    }
  })
}