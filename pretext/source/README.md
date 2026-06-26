# PreTeXt Book Structure

This directory contains the skeleton structure for a PreTeXt version of "Introduction to Data Science: Statistics and Prediction Algorithms Through Case Studies".

## Structure

The PreTeXt book follows the same organizational structure as the Quarto book defined in `_quarto.yml`:

### Main Files
- `project.ptx` - Project manifest file that configures build targets
- `source/main.ptx` - Main book structure with all parts and chapter includes

### Content Organization

#### Front Matter (`source/frontmatter/`)
- Preface
- Acknowledgments

#### Parts and Chapters

1. **Summary Statistics** (`source/summaries/`)
   - Introduction to Summary Statistics
   - Distributions
   - Numerical Summaries
   - Comparing Groups
   - Reading: Summary Statistics

2. **Probability** (`source/prob/`)
   - Introduction to Probability
   - Connecting Data and Probability
   - Discrete Probability
   - Continuous Probability
   - Random Variables
   - Sampling Models and Central Limit Theorem
   - Reading: Probability

3. **Statistical Inference** (`source/inference/`)
   - Introduction to Statistical Inference
   - Estimates and Confidence Intervals
   - Models
   - Bayesian Statistics
   - Hierarchical Models
   - Hypothesis Testing
   - Bootstrap
   - Reading: Statistical Inference

4. **Linear Models** (`source/linear-models/`)
   - Introduction to Linear Models
   - Regression
   - Linear Model Framework
   - Treatment Effect Models
   - Generalized Linear Models
   - Association is Not Causation
   - Multivariable Regression
   - Reading: Linear Models

5. **High Dimensional Data** (`source/highdim/`)
   - Introduction to High Dimensional Data
   - Matrices in R
   - Linear Algebra
   - Dimension Reduction
   - Regularization
   - Latent Factor Models
   - Reading: High Dimensional Data

6. **Machine Learning** (`source/ml/`)
   - Introduction to Machine Learning
   - Notation and Terminology
   - Evaluation Metrics
   - Conditionals and Smoothing
   - Resampling Methods
   - Algorithms
   - Machine Learning in Practice
   - Clustering
   - Reading: Machine Learning

#### Back Matter (`source/backmatter/`)
- References
- Index
- Colophon

## Building

To build the HTML version:
```bash
pretext build html
```

To build the PDF version:
```bash
pretext build pdf
```

## Publication Settings

Publication-specific settings are in `publication/publication.ptx`.

## Note

This is a skeleton structure. Chapter files contain only basic structure with placeholder content. Actual content from the Quarto book needs to be converted and added to these files.
