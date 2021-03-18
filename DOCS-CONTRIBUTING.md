## Contributing - Documentation
The Photon OS project team welcomes documentation contributions from the community.

To help you get started making contributions to Photon OS Documentation, we are providing this document to outline how the site is structured, how it gets updates, and how to contribute changes.

Documentation changes can be as large as adding a whoe set of new documents, or as small as fixing a single typo or a bad link.

## Scope and Structure

This branch ([photon-hugo](https://github.com/vmware/photon/tree/photon-hugo)) contains all content that is represented in [vmware.github.io/photon](https://vmware.github.io/photon). 

This includes:
- The Landing page: [vmware.github.io/photon](https://vmware.github.io/photon) 
- The Blog: [/photon/blog](https://vmware.github.io/photon/blog/) 
- The 4.0 docs: [/photon/docs](https://vmware.github.io/photon/docs/) 
- The 3.0 docs: in the new format [/photon/docs-v3](https://vmware.github.io/photon/docs-v3)
- The Old 'gitbook' static sites:
  - [v3 (Old)](https://vmware.github.io/photon/assets/files/html/3.0/)
  - [v1 and v2](https://vmware.github.io/photon/assets/files/html/1.0-2.0/)


### Folder Structure

A good overview of Hugo's directory structure can be found here:
[https://gohugo.io/getting-started/directory-structure/](https://gohugo.io/getting-started/directory-structure/)

`photon-hugo` branch

```
photon/
.
├── .github/workflows   <--- GitHub Action to build hugo site
├── CONTRIBUTING.md     <--- this document
├── LICENSE             <--- license file
├── assets              <--- logo and style override files
├── config.toml         <--- hugo config
├── content             <--- site content (markdown)
├── data/team/team.yaml <--- .yaml file describing the 'Team'
├── layouts/sitemap.xml <--- sitemap.xml
├── package-lock.json   <--- node package-lock file
├── package.json        <--- node package description
├── static              <--- custom js, old archived site
└── themes/photon-hugo  <--- contains the hugo theme/design
```

Within `/content/` we have language folders. Currently we only have `/content/en/` but the site is ready to support translations if any were made in the future.

```
photon/content/en/
.
├── _index.md           <--- Main content for landing page
├── blog                <--- Blog content
├── docs                <--- Current (v4) Docs content
├── docs-v3             <--- Old docs in new format
├── featured-background.png <--- The 'hero' image on the homepage.
└── search.md           <--- necessary for search feature

```

## How Publishing Works

The site itself is a 'static site', meaning there is no database, just HTML, CSS and Javascript, hosted via [GitHub Pages.](https://pages.github.com/). We chose to use [Hugo](https://gohugo.io) to deliver this (because it's fantastic, really!), with a modified version of the [Docsy](https://docsy.dev) 'theme'. Docsy is used for many open source projects including [Kubernetes](https://kubernetes.io/docs/home/), and is built with the help of [Bootstrap 4.5](https://getbootstrap.com).Changes to Docsy are listed in the /themes/photon-theme/CHANGES.md file.

The [Docsy Documentation](https://www.docsy.dev/docs/) has a varity of examples on the [various things](https://www.docsy.dev/docs/adding-content/) that can be done with content beyond simple text changes. 


### Making Changes The Super Simple Way

The Photon docs have the a feature to make changes to the source content of the repo directly from GitHub.

In the upper right corner of every [doc page](https://vmware.github.io/photon/docs/), there is an ***Edit this page*** link. When clicked, it will open an editor to make changes and allow you to quickly submit a pull request. No cloning, forking or otherwise dealing with git necessary.  If your changes are approved and merged into the branch, the site automation will kick in to rebuild and redeploy the site without any other intervention.

### Contributing Classic Way

For those familiar with using git and contributing to open source projects, this section should explain what you'll need to know about how the docs site is built so that you can make a meaningful contribution.

#### Important Thinngs to know: 
As mentioned, the `photon-hugo` branch contains all the necessary content and design to fully build the static html that lives at vmware.github.io/photon/. 

All content is written in Markdown, located in `/content/en/`, so changes should be made to these files and not to HTML directly, unless you're making changes to the template itself.

The markdown content gets converted into HTML via Hugo [by running the 'hugo' command](https://gohugo.io/getting-started/usage/). The GitHub Action essentially automates this for publishing.

There are 3 SCSS Pre-processors from Node.js which are required for local building. (autoprefixer, postcss-cli, postcss)

To make changes to existing content, you can simply modify your local copy with a text editor, save, do your `git commit` and `git push`, and finally submit a PR with your changes via your clone or through your fork.

If you want to create new content, there are some considerations to make regarding [Front Matter](https://gohugo.io/content-management/front-matter/) metadata, particularly around the `weight` attribute, which determines the order that the content gets displayed relative to the folder it's in within the left sidebar menu.

If you want to create a new file, you could either simply create the .md file, give it a name and the appropriate front matter, or use the [hugo cli](https://gohugo.io/commands/):

`hugo new docs/path/to/yourfile.md`

This will create the file with some default front matter to get started, but you'll need to fill in the author, linkName and date values, as well as assign it an appropriate weight.

For reference, just have a look at any of the other markdown content within /docs/ and you can see the front matter at the very top.



#### Local Site Build Prerequisites

If you want to build and test the site locally, you'll need the following:

- Hugo installed locally (min version 0.75, but always try to use the latest version)
- Node.js and the following node modules:
  - autoprefixer
  - postcss-cli
  - postcss
- A clone or fork of this repo with `photon-hugo` as the active branch.

Hugo and this site can be built on x86 or ARM64 CPUs thanks to Hugo having being compiled to run on ARM64. (i.e. it can be built on an M1 Mac or Raspberry Pi without emulation. yay!)

#### Installing Dependencies

- Firstly, you'll need to have Hugo installed. [Here is a link to Hugo's documentation](https://gohugo.io/getting-started/installing/) for more information on how to do that for your operating system.

- Install [Node.JS](https://nodejs.org/en/download/package-manager/) for your platform so you can use `npm`

- Install PostCSS dependencies via `npm`:
  - `cd` to the directory where your clone is located
  - run: `npm install -D autoprefixer postcss postcss-cli`

Once those are installed, you should be able to run `hugo` to build the site locally or `hugo server` to run the site in a live-reload local environment.

#### Building and Reviewing your Changes Locally

You can simply make changes to the Markdown content without needing to build the entire site locally. 

However, if you want to review the changes locally in what it's final form should look like, you would run the `hugo server` command from the root of the repo.

`hugo server` will build the site in real-time and present it to you at //localhost:1313.  Any changes that happen to markdown or design content will automatically be rebuild and loaded into the site when it detects that files have changed.

```
> hugo server
Start building sites … 

                   | EN   
-------------------+------
  Pages            | 667  
  Paginator pages  |   0  
  Non-page files   | 330  
  Static files     | 751  
  Processed images |   2  
  Aliases          |   1  
  Sitemaps         |   1  
  Cleaned          |   0  

Built in 1183 ms
Watching for changes in /<local folder path>/photon/{assets,content,data,layouts,package.json,static,themes}
Watching for config changes in /<local folder path>/photon/config.toml, /<local folder path>/photon/themes/photon-theme/config.toml
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at //localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```

If you want to simulate a full site generation, you can just run the `hugo` command. It will then render the entire site into the /public/ folder so you can go browse and open the local .html content directly. This folder is ignored by the repo through the .gitignore file.

## Submitting Changes

At a high level, contributions go through the following workflow:

- Clone or Fork and Pull vmware/photon 
- Make changes
- Commit changes
- Push changes to fork or origin
- Pull Request the change
  - Sign CLA if not already done
- Request gets reviewed
- Publish or suggest changes
  - Subsequent commits can be made to the same PR to address any changes needed without having to close the PR and then open a new one.


### CLA Bot

If you wish to contribute and you have not signed our Contributor License Agreement (CLA), our CLA-bot will take you through that process and then update the issue when you open a [Pull Request](https://help.github.com/articles/creating-a-pull-request). If you have questions about the CLA process, see our CLA [FAQ](https://cla.vmware.com/faq) or contact us through the GitHub issue tracker.