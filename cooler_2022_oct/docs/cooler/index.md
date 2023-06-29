# EIC-Cooler




## Optics

The optics are matched through the center of the cooling section.

View in tao:
```bash
tao -init $EIC_LATTICE/bmad/models/cooler/tao.init
```

![](images/tao_cooler_optics.png)



## Mode A table
[cooler_modea_20220424_table.csv](data/cooler_modea_20220424_table.csv)
![](images/cooler_modea_20220424_optics.png)


## Layout with IR2

```bash
tao -init $EIC_LATTICE/bmad/models/cooler/tao.init
```

```
place r00 floor4
x-s all -200 200
sc all -5 15
```

![](images/tao_cooler_ir2_layout.png)

[](https://www.classe.cornell.edu/~cem52/cooler/eic_cooler_ir2.html)



Also see the [Interactive Layout](https://www.classe.cornell.edu/~cem52/cooler/eic_cooler_ir2.html)
