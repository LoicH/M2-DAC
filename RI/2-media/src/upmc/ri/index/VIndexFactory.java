package upmc.ri.index;

import java.util.List;



public class VIndexFactory {
	public static double[] computeBow(ImageFeatures ib) {
		List<Integer> words = ib.getwords();
		double[] target = new double[words.size()];
		for (int i = 0; i < target.length; i++) {
		    target[i] = words.get(i);
		 }
		return target;
		
	}
}