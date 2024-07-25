function noembed(url) {
  var endpoint = '//noembed.com/embed?';

  if (!!url.length) {
    endpoint += 'url=' + encodeURIComponent(url);
    return '<div class="noembed-wrapper" data-url="' + endpoint + '">' + url + '</div>';
  }

  return url;
}

module.exports = {
  website: {
    assets: './assets',
    js: ['scripts.js'],
    css: ['style.css']
  },
  filters: {
    noembed: noembed,
    video: noembed,
  }
};
