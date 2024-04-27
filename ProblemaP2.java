import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Scanner;

public class ProblemaP2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int numCasos = scanner.nextInt();
        for (int caso = 0; caso < numCasos; caso++) {
            int n = scanner.nextInt();
            int w1 = scanner.nextInt();
            int w2 = scanner.nextInt();
            ArrayList<Tuple<Integer, String>> elementos = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                int masa1 = scanner.nextInt();
                String carga1 = scanner.next();
                int masa2 = scanner.nextInt();
                String carga2 = scanner.next();
                elementos.add(new Tuple<>(masa1, carga1));
                elementos.add(new Tuple<>(masa2, carga2));
            }

            // Procesamiento
            ArrayList<Tuple<ArrayList<Tuple<Integer, String>>, Integer>> compuestos = formarCompuestos(elementos, w1, w2);

            // Salida de resultados
            if (!compuestos.isEmpty()) {
                Tuple<ArrayList<Tuple<Integer, String>>, Integer> compuestoMinimo = Collections.min(compuestos, new MyComparator());
                StringBuilder sb = new StringBuilder();
                for (Tuple<Integer, String> atom : compuestoMinimo.first) {
                    sb.append("(").append(atom.first).append(" ").append(atom.second).append(") ");
                }
                sb.append(compuestoMinimo.second);
                System.out.println(sb.toString());
            } else {
                System.out.println("NO SE PUEDE");
            }
        }
        scanner.close();
    }

    static class Tuple<X, Y> {
        public final X first;
        public final Y second;
        public Tuple(X first, Y second) {
            this.first = first;
            this.second = second;
        }
    }

    static class MyComparator implements Comparator<Tuple<ArrayList<Tuple<Integer, String>>, Integer>> {
        @Override
        public int compare(Tuple<ArrayList<Tuple<Integer, String>>, Integer> o1, Tuple<ArrayList<Tuple<Integer, String>>, Integer> o2) {
            return Integer.compare(o1.second, o2.second);
        }
    }

    static ArrayList<Tuple<ArrayList<Tuple<Integer, String>>, Integer>> formarCompuestos(ArrayList<Tuple<Integer, String>> elementos, int w1, int w2) {
        ArrayList<Tuple<ArrayList<Tuple<Integer, String>>, Integer>> compuestos = new ArrayList<>();
        ArrayList<ArrayList<Tuple<Integer, String>>> permutaciones = new ArrayList<>();
        generarPermutaciones(elementos, new ArrayList<>(), permutaciones);
        for (ArrayList<Tuple<Integer, String>> permutacion : permutaciones) {
            boolean compuestoValido = true;
            int energiaTotal = 0;
            for (int i = 0; i < permutacion.size() - 1; i++) {
                Tuple<Integer, String> atom1 = permutacion.get(i);
                Tuple<Integer, String> atom2 = permutacion.get(i + 1);
                int energia = calcularEnergia(atom1, atom2, w1, w2);
                if (energia == 0) {
                    compuestoValido = false;
                    break;
                }
                energiaTotal += energia;
            }
            if (compuestoValido) {
                compuestos.add(new Tuple<>(permutacion, energiaTotal));
            }
        }
        return compuestos;
    }

    static void generarPermutaciones(ArrayList<Tuple<Integer, String>> elementos, ArrayList<Tuple<Integer, String>> permutacionActual, ArrayList<ArrayList<Tuple<Integer, String>>> permutaciones) {
        if (elementos.isEmpty()) {
            permutaciones.add(new ArrayList<>(permutacionActual));
            return;
        }
        for (int i = 0; i < elementos.size(); i++) {
            Tuple<Integer, String> elemento = elementos.get(i);
            ArrayList<Tuple<Integer, String>> nuevosElementos = new ArrayList<>(elementos);
            nuevosElementos.remove(i);
            ArrayList<Tuple<Integer, String>> nuevaPermutacion = new ArrayList<>(permutacionActual);
            nuevaPermutacion.add(elemento);
            generarPermutaciones(nuevosElementos, nuevaPermutacion, permutaciones);
        }
    }

    static int calcularEnergia(Tuple<Integer, String> atom1, Tuple<Integer, String> atom2, int w1, int w2) {
        int m1 = atom1.first;
        int m2 = atom2.first;
        String c1 = atom1.second;
        String c2 = atom2.second;
        if (c1.equals(c2)) {
            return 1 + Math.abs(m1 - m2) % w1;
        } else {
            return w2 - Math.abs(m1 - m2) % w2;
        }
    }
}
