# ------ Load required libraries ------
library(ggtree)
library(ggplot2)

# ------ Define the function to create the ggtree plot ------
create_ggtree_plot <- function(tree, tip_label_size, tip_label_color, branch_size, branch_color, x_limits, y_limits,
                               hjust = 0, vjust = 0.5, angle = 0, theme_func = theme_tree2) {
  # Parameter verification
  if (!is.numeric(tip_label_size) || tip_label_size <= 0) {
    stop("tip_label_size must be a positive number.")
  }
  if (!is.numeric(branch_size) || branch_size <= 0) {
    stop("branch_size must be a positive number.")
  }
  
  ggtree_plot <- ggtree(tree, branch.length = "none") +
    geom_tiplab(size = tip_label_size, color = tip_label_color, hjust = hjust, vjust = vjust, angle = angle) +
    expand_limits(x = x_limits, y = y_limits) +
    geom_tree(size = branch_size, color = branch_color) +
    theme_func()
    
  return(ggtree_plot)
}

# ------ Data checking and preprocessing ------

# Define tree file path as a parameter for flexibility
tree_file <- function(tree_file_path = "phylo.tree") {
  if (!file.exists(tree_file_path)) {
    stop("Tree file does not exist.")
  }
  return(tree_file_path)
}

# Read tree file with tryCatch
read_tree_file <- function(tree_file_path) {
  tryCatch({
    tree <- read.tree(tree_file_path)
    return(tree)
  }, error = function(e) {
    stop(sprintf("Unable to read tree file '%s': %s", tree_file_path, e$message))
  })
}

# ------ Set plotting parameters ------

# Adjust tip label size and color
tip_label_size <- 3
tip_label_color <- "blue"

# Adjust branch size and color
branch_size <- 1.5
branch_color <- "darkgreen"

# Adjust plot area size
x_limits <- c(-10, 10)
y_limits <- c(-5, 5)

# Output file path and dimensions
output_file <- "tree_plot.pdf"
output_width <- 20
output_height <- 10

# ------ Use the function to create the plot ------
create_and_save_plot <- function(tree_file_path, output_file_path) {
  tree <- read_tree_file(tree_file_path)
  
  ggtree_plot <- create_ggtree_plot(
    tree,
    tip_label_size,
    tip_label_color,
    branch_size,
    branch_color,
    x_limits,
    y_limits
  )
  
  # Display and save the plot
  print(ggtree_plot)
  
  tryCatch({
    ggsave(output_file_path, plot = ggtree_plot, width = output_width, height = output_height)
    cat(sprintf("Plot successfully saved to '%s'\n", output_file_path))
  }, error = function(e) {
    cat(sprintf("Unable to save plot to '%s': %s\n", output_file_path, e$message))
  })
}

# ------ Execute the script part ------
tree_file_path <- tree_file()
create_and_save_plot(tree_file_path, output_file)
