import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import h5py
from pmd_beamphysics import ParticleGroup
from distgen import Generator


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
      avg_t:
        units: ns
        value: 0.0
      sigma_t:
        units: ns
        value: {sig_t}
      type: interp
      method: spline
      Pt:
        pt00: 0
        pt01: {p1}
        pt02: {p2}
        pt03: {p3}
        pt04: {p4}
        pt05: {p5}
        pt06: {p6}
        pt07: {p7}
        pt08: {p8}
        pt09: 0
    total_charge:
      units: nC
      value: 1
        
    """
    
    ID = abs(hash(DISTGEN_IN))
    D = Generator(DISTGEN_IN)
    D.run()
    P0 = D.particles
    P0.write(f"temp/{ID}.h5")
    return ID

def track(ID):
    subprocess.run(["/nfs/user/nw285/bmad_para/production/bin/tao", "-noplot", "-beam_init_position_file", f"temp/{ID}.h5", "-command", f"set global track_type = beam; write beam -at end temp/{ID}end.h5; exit"])
    P = ParticleGroup(f"temp/{ID}end.h5")
    return P

def rms(arr, target):
    return np.sqrt(np.average( (arr-target)**2 ))

def avg(dat, weights):
    """Statistical average"""
    if np.isscalar(dat): 
        return dat
    return np.average(dat, weights=weights)
    
def std(dat, weights):
    """Standard deviation (actually sample)"""
    if np.isscalar(dat):
        return 0
    avg_dat = avg(dat, weights)
    return np.sqrt(np.average( (dat - avg_dat)**2, weights=weights))

def uncorrelated_slice_stat(P,var,stat,n_slice,slice_key='t'):
    stat_fun = {'min':np.min, 'max':np.max, 'mean':avg, 'sigma':std}
    slices = particle_group.split(n_chunks=n_slice, key=slice_key)
    
    slice_stats = np.zeros(len(slices))
    
    for ii, s in enumerate(slices):
        
        cov = s.cov(slice_key, var)
        
        v = s[var] - (cov[0,1]/cov[0,0])*s[f'delta_{slice_key}']
        
        slice_stats[ii] = stat_fun[stat](v, s.weight)
        
        
    return slice_stats

def calculate_error(P):
    targets = [10, 1e-4, 2.8e-6]
    slice_stat = P.slice_statistics('sigma_pz', 'norm_emit_x', n_slice=50)
    slice_stat['sigma_pz'] /= P['mean_pz']
    center = ((slice_stat['mean_t'] > (P['mean_t']-P['sigma_t'])) & (slice_stat['mean_t'] < (P['mean_t']+P['sigma_t'])) )

    current = rms(slice_stat['current'][center], targets[0])
    slice_pz = rms(slice_stat['sigma_pz'][center], targets[1])
    slice_emit_x = rms(slice_stat['norm_emit_x'][center], targets[2])
    return current/targets[0], slice_pz/targets[1], slice_emit_x/targets[2]

def evaluate_splice_flat(inputs: dict) -> dict:
    ID = generate_initial_particles(inputs)
    P = track(ID)
    current, slice_pz, slice_emit_x = calculate_error(P)
    return {'ID': ID, 'current': current, 'slice_pz': slice_pz, 'slice_emit_x': slice_emit_x, 'n_alive': P.n_alive}

def test(inputs: dict) -> dict:
    return {'current': 0.1, 'slice_pz': 0.15, 'slice_emit_x': 0.2, 'n_alive': 10000}

def main():
    print(evaluate_splice_flat({'p1':1,'p2':1,'p3':1,'p4':1,'p5':1,'p6':1,'p7':1,'p8':1, 'sig_t':0.03}))

if __name__=='__main__':
    main()
