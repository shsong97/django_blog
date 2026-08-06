$(document).ready(function () {
  function fillList(selector, url, builder) {
    $.ajax({
      url: url,
      dataType: 'json',
      success: function (result) {
        var message = '';
        for (var i in result) {
          message += builder(result[i]);
        }
        $(selector).html(message || '<li style="color:var(--ig-muted);font-size:0.88rem;">—</li>');
      },
      error: function () {
        $(selector).html('<li style="color:var(--ig-muted);font-size:0.88rem;">—</li>');
      }
    });
  }

  fillList('#favorite_article', '/blog/favorite/', function (item) {
    return "<li><a href='/blog/" + item.blog_id + "/'><span>" + item.blog_title + "</span><strong>" + item.like_count + "</strong></a></li>";
  });

  fillList('#recent_article', '/blog/archive/', function (item) {
    return "<li><a href='/blog/list/" + item.year + "/" + item.month + "/'><span>" + item.year + "/" + item.month + "</span><strong>" + item.cnt + "</strong></a></li>";
  });

  $(document).on('click', '.blog-like-btn', function () {
    var button = $(this);
    var blogId = button.data('blog-id');
    var post = button.closest('.ig-post');
    $.ajax({
      url: '/blog/' + blogId + '/like/',
      dataType: 'json',
      success: function (result) {
        button.addClass('is-liked');
        post.find('.blog-like-count').text(result.result);
      }
    });
  });
});
