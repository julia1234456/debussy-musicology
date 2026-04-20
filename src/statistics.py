import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import pearsonr, spearmanr, entropy

def compute_test_matrix(
        A, B, test_name,
        names_A=None, names_B=None,
        visualize=True,
        figsize=(8,8),
        display_significant=False,  
        alpha=0.10):   
    """
    Compute a pairwise statistical comparison matrix between two collections of vectors.

    For each pair (a ∈ A, b ∈ B), computes either a correlation coefficient or a
    divergence measure, then optionally renders an annotated heatmap.

    Supported tests:
      - 'pearson'       : Pearson linear correlation coefficient + p-value.
      - 'spearman'      : Spearman rank correlation coefficient + p-value.
      - 'kl_divergence' : KL divergence D_KL(a || b); no p-value is defined.  
    """      
    
    # --- default names -----------------------------------------------------
    if names_A is None:
        names_A = [f"A{i}" for i in range(len(A))]
    if names_B is None:
        names_B = [f"B{i}" for i in range(len(B))]
    if len(names_A) != len(A) or len(names_B) != len(B):
        raise ValueError("Length of names_A / names_B must match A / B.")

    # --- compute statistics ------------------------------------------------
    stat_mat, res_mat = [], []
    for a in A:
        row_stats, row_vals = [], []
        for b in B:
            if test_name == "pearson":
                stat, p = pearsonr(a, b)
            elif test_name == "spearman":
                stat, p = spearmanr(a, b)
            elif test_name == "kl_divergence":
                a_norm = np.asarray(a) / np.sum(a)
                b_norm = np.asarray(b) / np.sum(b)
                stat, p = entropy(a_norm, b_norm), None
            else:
                raise ValueError("test_name must be 'pearson', 'spearman', or 'kl_divergence'")
            row_stats.append((stat, p))
            row_vals.append(stat)
        res_mat.append(row_stats)
        stat_mat.append(row_vals)

    # --- visualisation -----------------------------------------------------
    if visualize:
        vals = np.array(stat_mat)
        plt.figure(figsize=figsize)
        cmap = None

        if test_name in ("pearson", "spearman"):
            cmap = plt.cm.RdYlGn
            vmin, vmax = -1, 1
        else:
            cmap = plt.cm.Greens
            vmin, vmax = 0, np.max(vals) if np.max(vals) > 0 else 1

        im = plt.imshow(vals, cmap=cmap, vmin=vmin, vmax=vmax)

        plt.xticks(range(len(B)), names_B, rotation=45, ha="right")
        plt.yticks(range(len(A)), names_A)
        plt.title(test_name.replace('_', ' ').title())

        for i in range(len(A)):
            for j in range(len(B)):
                stat, p = res_mat[i][j]
                if p is not None:
                    if not display_significant or (p <= alpha):
                        text = f"{stat:.2f}\n(p={p:.2g})"
                    else:
                        text = ""
                else:
                    text = f"{stat:.2f}"
                plt.text(j, i, text, ha="center", va="center", color="black", fontsize=9)

        plt.colorbar(im, label=("Correlation" if test_name != "kl_divergence" 
                                else "KL Divergence"))
        plt.tight_layout()
        plt.show()

    return res_mat
### KL_divergence 
def kl_divergence(p, q, epsilon=1e-10):
    """
    Compute KL divergence D_KL(P || Q)
    p, q: Input histograms (arrays), should be normalized to sum to 1
    epsilon: Small value to avoid division by zero or log(0)
    """
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    


    # Avoid log(0) and division by zero
    p = np.clip(p, epsilon, 1)
    q = np.clip(q, epsilon, 1)

    return np.sum(p * np.log(p / q))