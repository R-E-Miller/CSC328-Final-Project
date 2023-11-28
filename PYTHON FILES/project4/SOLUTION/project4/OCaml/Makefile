all: project4

project4: project4.ml
	ocamlopt -o project4 unix.cmxa project4.ml

.PHONY: clean

clean:
	rm -f project4
	rm -f *.o *.cmi *.cmx p4
