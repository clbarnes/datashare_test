# Connectome

## Format

A comma-separated value edge list file with the following columns:

`source,target,transmitter,receptor,minimum_distance,source_doi,target_doi`

## Usage

You can:

* Use the  link on the right to download a .zip including the file
* Use `git clone git@github.com:clbarnes/datashare_test.git` from your terminal to clone this repository (good if you want to contribute and/or have easy access to updates)
* Use `wget https://raw.githubusercontent.com/clbarnes/datashare_test/master/edgelist.csv` from your console
* Click on `edgelist.csv` and then `Raw`, and copy and paste the text

## Contributing

If you would like to contribute to the data set:
1. [Fork this repository](https://help.github.com/articles/fork-a-repo/) with your own github account
2. Edit `data/edgelist.csv` with your changes
3. [Push your changes](https://help.github.com/articles/pushing-to-a-remote/) to your forked repository
4. [Raise a pull request](https://help.github.com/articles/using-pull-requests/) to integrate your changes into `master` for the maintainer to review.

## FAQ

### Why edge lists?

Edge lists are unambiguous, cross-platform and human-readable. They can represent multigraphs (with parallel edges) and require little boilerplate code to interpret. As one line is one edge (unlike an adjacency matrix), changes are easy to track between versions, and play very nicely with git.

### Why git?

Whenever data is shared openly and updated regularly, it is vital that it is versioned. Git makes it easy to see exactly when the data was updated, what was changed, and who updated it. It efficiently compresses old data sets as linewise differences from the current `master` branch.

### Why GitHub?

GitHub is free, commonly used by open source and open science projects, and provides a number of tools for reviewing changes in data, viewing the history, and allowing others to contribute in a controlled and secure manner. GitHub also provides [graphical](https://windows.github.com/) [applications](https://mac.github.com/) for less CLI-oriented users!
