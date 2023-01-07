package prog.optim.cp;

import com.google.ortools.sat.CpModel;
import com.google.ortools.sat.CpSolver;
import com.google.ortools.sat.CpSolverStatus;
import com.google.ortools.sat.IntVar;
import com.google.ortools.sat.LinearExpr;
import com.google.ortools.sat.LinearExprBuilder;
import com.google.ortools.Loader;
import static java.util.Arrays.stream;

import java.util.logging.Logger;

// To prevent date time in logs add the VM argument -Djava.util.logging.SimpleFormatter.format="%4$s: %5$s%n"
public class MultiObjExample {

	private static void showResults(CpSolver solver, CpModel model, IntVar[] varlist, String[] names) {
		CpSolverStatus status = solver.solve(model);

		boolean found = false;
		if (status == CpSolverStatus.FEASIBLE) {
			logger.info("Found a feasible solution.");
			found = true;
		} else if (status == CpSolverStatus.OPTIMAL) {
			logger.info("Found an optimal solution.");
			found = true;
		} else {
			logger.info("Unable to get a solution");
		}

		if (found) {
			logger.info(String.format("Maximum of objective function: %f", solver.objectiveValue()));
			for (int i = 0; i < varlist.length; ++i) {
				logger.info(String.format("%s = %d", names[i], solver.value(varlist[i])));
			}
		} else {
			logger.info("No solution found.");
		}
	}

	private static LinearExprBuilder append(LinearExprBuilder builder, IntVar[] varlist, long[] coeffs, boolean add) {
		int factor = add ? 1 : -1;

		for (int i = 0; i < varlist.length; ++i) {
			builder.addTerm(varlist[i], factor * coeffs[i]);
		}

		return builder;
	}

	public static void main(String[] args) {
		Loader.loadNativeLibraries();
		CpModel model = new CpModel();
		int varUpperBound = stream(new int[] { 50, 45, 37 }).max().getAsInt();
		final String[] names = { "x", "y", "z" };

		IntVar x = model.newIntVar(0, varUpperBound, names[0]);
		IntVar y = model.newIntVar(0, varUpperBound, names[1]);
		IntVar z = model.newIntVar(0, varUpperBound, names[2]);
		IntVar[] varlist = { x, y, z };

		model.addLessOrEqual(LinearExpr.weightedSum(varlist, new long[] { 2, 7, 3 }), 50);
		model.addLessOrEqual(LinearExpr.weightedSum(varlist, new long[] { 3, -5, 7 }), 45);
		model.addLessOrEqual(LinearExpr.weightedSum(varlist, new long[] { 5, 2, -6 }), 37);

		CpSolver solver = new CpSolver();
		model.maximize(LinearExpr.weightedSum(new IntVar[] { x, y, z }, new long[] { 2, 2, 3 }));
		showResults(solver, model, varlist, names);

		model.minimize(LinearExpr.weightedSum(new IntVar[] { x, y, z }, new long[] { 1, -1, 0 }));
		showResults(solver, model, varlist, names);

		LinearExprBuilder builder = LinearExpr.newBuilder();

		// Adding two objective functions.
		builder = append(builder, varlist, new long[] { 2, 2, 3 }, true);
		builder = append(builder, varlist, new long[] { 1, -1, 0 }, false);

		LinearExpr obj = builder.build();
		model.maximize(obj);
		showResults(solver, model, varlist, names);
	}

	private static Logger logger = Logger.getLogger(MultiObjExample.class.getName());
}
