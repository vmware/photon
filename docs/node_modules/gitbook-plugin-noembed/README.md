# Gitbook plugin Noembed

Get any video or iframe card supported by [Noembed](https://noembed.com/#supported-sites). (Vimeo, YouTube, Facebook, Twitter, Instagram, etc)

*If the sites you need to embed are not supported by Noembed, you can try [gitbook-plugin-iframely](https://github.com/1cgonza/gitbook-plugin-iframely). They claim to support 1,800+ sites but you need at least a free account to get an API key.*

## Installation
Add "noembed" to your plugins in `book.json`.

```js
{
  "plugins": ["noembed"]
}
```

## Usage
- You can use two filters: `noembed` or `video`. *(At the moment they both do exactly the same)*
- Make sure you wrap your URL around single or double quotes.

```md
{{ 'https://vimeo.com/31942602' | noembed }}

or

{{ 'https://vimeo.com/31942602' | video }}
```

