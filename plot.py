import argparse
import os
import os.path as op
import subprocess
import sys

def process(output_dir, dockq_files, mean_dockq_files, correlation_files, report_basename):
    """
    Calls rmarkdown::render with file lists as parameters.
    """
    rmd_path = op.join(sys.path[0], 'plotting_comb.Rmd')
    output_dir_abs = op.abspath(output_dir)
    dockq_files = [op.abspath(f) for f in dockq_files]
    mean_dockq_files = [op.abspath(f) for f in mean_dockq_files]
    correlation_files = [op.abspath(f) for f in correlation_files]

    # Pass file lists as parameters to RMarkdown
    rscript = (
        f"rmarkdown::render('{rmd_path}', "
        f"params = list("
        f"output_dir = '{output_dir_abs}', "
        f"dockq_files = I(c({', '.join([f'\"{f}\"' for f in dockq_files])})), "
        f"mean_dockq_files = I(c({', '.join([f'\"{f}\"' for f in mean_dockq_files])})), "
        f"correlation_files = I(c({', '.join([f'\"{f}\"' for f in correlation_files])}))"
        f"), "
        f"output_file = '{report_basename}', "
        f"output_dir = '{output_dir_abs}')"
    )

    subprocess.run(
        ["Rscript", "-e", rscript],
        cwd=output_dir,
        check=True
    )

def main():
    parser = argparse.ArgumentParser(description='Run combined DockQ plotting.')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory.')
    parser.add_argument('--metrics.dockq', type=str, nargs='+', required=True, help='DockQ metrics files.')
    parser.add_argument('--metrics.mean_dockq', type=str, nargs='+', required=True, help='Mean DockQ metrics files.')
    parser.add_argument('--correlation.scores', type=str, nargs='+', required=True, help='Correlation scores files.')
    parser.add_argument('--name', type=str, default='dockq_report.html', help='Output HTML report name.')

    args = parser.parse_args()

    dockq_files = getattr(args, 'metrics.dockq')
    mean_dockq_files = getattr(args, 'metrics.mean_dockq')
    correlation_files = getattr(args, 'correlation.scores')

    process(
        output_dir=args.output_dir,
        dockq_files=dockq_files,
        mean_dockq_files=mean_dockq_files,
        correlation_files=correlation_files,
        report_basename='dockq_report.html'  
    )

if __name__ == "__main__":
    main()