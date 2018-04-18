# install the required packages if you don't alreadyy have them
#
# install.packages(c('ggplot2', 'magrittr', 'reshape2'),
#                  repos='https://cloud.r-project.org/')

library(ggplot2)
library(magrittr)
library(reshape2)

source('wallace-helper.R')



shannon <- compiler::cmpfun(function(clusters, base=2) {
    # Calculates the Shannon Entropy for a group of clusters
    # uses base 2, returning bits by default

    p_i <- function(i) {
        sum(clusters == i) / length(clusters)
    }

    N <- unique(clusters)

    -sum(sapply(N, function(i) p_i(i) * log(p_i(i), base = base)))
 })

neighbour_awc <- compiler::cmpfun(function(clusts, i) {
    # Calculates the Adjusted Wallace Coefficent of the
    # ith column versus the i-1th column

    cur <- clusts[,i]

    if ((i - 1) == 0 || length(unique(cur)) == 1) {
        result <- NA

    } else {

        result <- adj_wallace(cur, clusts[, i-1]) %>%
                  use_series('Adjusted_Wallace_A_vs_B')
    }

    result
})

singleton_proportion <- function(x) {
    # Determines what proportion of clusters
    # have only a single member genome

    singletons <- sum(table(x) == 1)

    p_singleton <- singletons / length(unique(x))

    p_singleton

}

stats_df <- function(clusters) {
    # Calculates various statistics for clusters,
    # and binds them together in a data.frame

    thresholds <-
        clusters %>%
        colnames %>%
        gsub(pattern = 'h_', replacement = '') %>%
        as.integer

    entropy <- sapply(clusters, shannon)

    nawc <-
        clusters %>%
        seq_along %>%
        sapply(neighbour_awc, clusts=clusters)

    n_clusts <- sapply(clusters, function(x) length(unique(x)))

    # p_singletons <- sapply(clusters, singleton_proportion)

    df <- data.frame('Threshold' = thresholds,
                     'Neighbour AWC' = nawc,
                     'Shannon (bits)' = entropy,
                     # 'Number of Clusters' = n_clusts,
                     # 'Proportion of Singleton Clusters' = p_singletons,
                     check.names = FALSE)
    df
}

df <- stats_df(goeburst)


goeburst_path <- 'campy_strain_st.tsv'

goeburst <-
    goeburst_path %>%
    read.table(sep = '\t', row.names = 1, header = TRUE, check.names = FALSE)

m <- melt(df, id.vars = 'Threshold')
tiff(filename='campy_stability.tiff',
     res = 600,
     width = 600 * 8.5,
     height = 600 * 5)
ggplot(m, aes(x = Threshold, y = value)) +
    geom_step() +
    facet_grid(variable ~ ., scales = 'free_y', switch = 'y') +
    labs(x = 'goeBURST Threshold', y = '')

dev.off()

goeburst_path <- 'salmy_strain_st.tsv'

goeburst <-
    goeburst_path %>%
    read.table(sep = '\t', row.names = 1, header = TRUE, check.names = FALSE)

m <- melt(df, id.vars = 'Threshold')
tiff(filename='salmy_stability.tiff',
     res = 600,
     width = 600 * 8.5,
     height = 600 * 5)
ggplot(m, aes(x = Threshold, y = value)) +
    geom_step() +
    facet_grid(variable ~ ., scales = 'free_y', switch = 'y') +
    labs(x = 'goeBURST Threshold', y = '')

dev.off()
