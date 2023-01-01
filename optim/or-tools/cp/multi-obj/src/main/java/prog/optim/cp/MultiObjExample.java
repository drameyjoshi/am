package prog.optim.cp;
import com.google.ortools.sat.CpModel;
import com.google.ortools.sat.CpSolver;
import com.google.ortools.sat.CpSolverStatus;
import com.google.ortools.sat.IntVar;
import com.google.ortools.sat.LinearExpr;
import com.google.ortools.sat.LinearExprBuilder;
import com.google.ortools.Loader;
import static java.util.Arrays.stream;

public class MultiObjExample {

	private static void showResults(CpSolver solver, CpModel model, IntVar x, IntVar y, IntVar z) {
		CpSolverStatus status = solver.solve(model);

		if (status == CpSolverStatus.OPTIMAL || status == CpSolverStatus.FEASIBLE) {
			System.out.printf("Maximum of objective function: %f%n", solver.objectiveValue());
			System.out.println("x = " + solver.value(x));
			System.out.println("y = " + solver.value(y));
			System.out.println("z = " + solver.value(z));
		} else {
			System.out.println("No solution found.");
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

		IntVar x = model.newIntVar(0, varUpperBound, "x");
		IntVar y = model.newIntVar(0, varUpperBound, "y");
		IntVar z = model.newIntVar(0, varUpperBound, "z");

		model.addLessOrEqual(LinearExpr.weightedSum(new IntVar[] { x, y, z }, new long[] { 2, 7, 3 }), 50);
		model.addLessOrEqual(LinearExpr.weightedSum(new IntVar[] { x, y, z }, new long[] { 3, -5, 7 }), 45);
		model.addLessOrEqual(LinearExpr.weightedSum(new IntVar[] { x, y, z }, new long[] { 5, 2, -6 }), 37);

		CpSolver solver = new CpSolver();
		model.maximize(LinearExpr.weightedSum(new IntVar[] { x, y, z }, new long[] { 2, 2, 3 }));
		showResults(solver, model, x, y, z);

		model.minimize(LinearExpr.weightedSum(new IntVar[] { x, y, z }, new long[] { 1, -1, 0 }));
		showResults(solver, model, x, y, z);

		LinearExprBuilder builder = LinearExpr.newBuilder();
		IntVar[] varlist = { x, y, z };

		// Adding two objective functions.
		builder = append(builder, varlist, new long[] { 2, 2, 3 }, true);
		builder = append(builder, varlist, new long[] { 1, -1, 0 }, false);

		LinearExpr obj = builder.build();
		model.maximize(obj);
		showResults(solver, model, x, y, z);
	}

}
