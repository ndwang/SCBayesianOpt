import os
import matplotlib.pyplot as plt
import numpy as np
import h5py
from pmd_beamphysics import ParticleGroup, particle_paths
from distgen import Generator
from distgen.metrics import kullback_liebler_div, res2
from distgen.physical_constants import unit_registry
from distgen.dist import SuperGaussian

L = 200*unit_registry('ps')
avg_t_sg = 0*unit_registry('ps')
sigma_t_sg = L/np.sqrt(12)
sg = SuperGaussian('t', avg_t=avg_t_sg, sigma_t=sigma_t_sg, p=12)
tsg, Psg = sg.get_x_pts(), sg.pdf()

AC_GUN_IN = """
    n_particle: 10000
    random_type: hammersley

    start:
        type: cathode
        MTE:
            units: meV
            value: 250

    total_charge:
        units: pC
        value: 50

    r_dist:
        type: radial_uniform
        max_r:
            units: mm
            value: 0.5

    t_dist:
        Pt:
            pt01: {p1}
            pt02: {p2}
            pt03: {p3}
            pt04: {p4}
        avg_t:
            units: ps
            value: 0.0
        method: spline
        sigma_t:
            units: ps
            value: 10
        type: interp  
    """
COOLER_IN = """
    n_particle: 10000
    r_dist:
      truncation_fraction:
        units: dimensionless
        value: 0.5
      truncation_radius:
        units: mm
        value: 2.3319043122
      type: rg
    random_type: hammersley
    start:
      MTE:
        units: meV
        value: 130
      type: cathode
    t_dist:
      Pt:
        pt01: {p1}
        pt02: {p2}
        pt03: {p3}
        pt04: {p4}
      avg_t:
        units: ps
        value: 0.0
      method: spline
      sigma_t:
        units: ps
        value: 0.08287285705
      type: interp
    total_charge:
      units: nC
      value: 1
    """
def read_particles(FILE):
    with h5py.File(FILE, 'r') as h5:
        ppaths = particle_paths(h5)
        Plist = [ParticleGroup(h5[g]) for g in ppaths]
    print(f"read {FILE}")
    return Plist

def array_to_middle_values(arr):
    ret = list()
    for i in range(len(arr)-1):
        ret.append((arr[i]+arr[i+1])/2)
    return np.array(ret)

def generate_initial_particles(inputs: dict):
    p1 = inputs['p1']
    p2 = inputs['p2']
    p3 = inputs['p3']
    p4 = inputs['p4']
    p5 = inputs['p5']
    p6 = inputs['p6']
    p7 = inputs['p7']
    p8 = inputs['p8']
    sig_t = inputs['sig_t']

    DISTGEN_IN = f"""
    n_particle: 10000
    r_dist:
      max_r:
        units: mm
        value: 3.7811487497
      type: radial_uniform
    random_type: hammersley
    start:
      MTE:
        units: meV
        value: 130
      type: cathode
    t_dist:
      avg_t:
        units: ns
        value: 0.0
      sigma_t:
        units: ns
        #value: 0.02886751345
        value: {sig_t}
      type: interp
      method: spline
      Pt:
        pt01: {p1}
        pt02: {p2}
        pt03: {p3}
        pt04: {p4}
        pt05: {p5}
        pt06: {p6}
        pt07: {p7}
        pt08: {p8}
    total_charge:
      units: nC
      value: 1
        
    """
    
    ID = abs(hash(DISTGEN_IN))
    D = Generator(DISTGEN_IN)
    D.run()
    P0 = D.particles
    P0.write(f"temp/{ID}.h5")
    print(f"wrote temp/{ID}.h5")
    return ID

def track(ID):
    os.system(f"/nfs/user/nw285/bmad_para/production/bin/tao -init cooler/tao_opt.init -noplot -beam_init_position_file temp/{ID}.h5 -command \"set beam_init n_particle = 10000; set global track_type = beam; write beam -at end temp/{ID}end.h5; exit\"")
    P = read_particles(f"temp/{ID}end.h5")[-1]
    #os.system(f"rm temp/{ID}.h5")
    return P

def calculate_error(P):
    datar = list()
    alive = (P['status']==1)
    datar.append(P['t'][alive])
    d = np.histogram(datar, bins=100, density=True)

    ps = d[0]
    ts = array_to_middle_values(d[1])
    ts = ts - np.average(ts)
    ts = ts * 1e12 * unit_registry('ps')
    ps = ps / 1e12 / unit_registry('ps')

    #entropy = kullback_liebler_div(ts, ps, tsg, Psg)
    entropy = res2(ts,ps,tsg,Psg)
    return entropy

def evaluate_splice_flat(inputs: dict) -> dict:
    ID = generate_initial_particles(inputs)
    P = track(ID)
    #ID = 1
    #P = read_particles('end.h5')[-1]
    entropy = calculate_error(P)
    emit_x = P['norm_emit_x']
    print(ID, entropy)
    return {'entropy': entropy, 'norm_emit_x': emit_x, 'ID': ID, 'n_alive': P.n_alive}

def main():
    print(evaluate_splice_flat({'p1':1,'p2':1,'p3':1,'p4':1,'p5':1,'p6':1,'p7':1,'p8':1, 'sig_t':0.03}))

if __name__=='__main__':
    main()
