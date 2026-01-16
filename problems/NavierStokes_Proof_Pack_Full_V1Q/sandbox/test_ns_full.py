#!/usr/bin/env python3
# Navier-Stokes full sandbox (automatic).
# - Taylor-Green vortex 2D pseudo-solver
# - Tracks energy/enstrophy, CFL, convergence hints
# - Exports CSV, PNG, manifest with SHA256

import argparse, os, csv, time, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils import sha256_of_file, write_manifest

def init_tg(nx, ny, L=2*np.pi):
    x = np.linspace(0,L,nx,endpoint=False)
    y = np.linspace(0,L,ny,endpoint=False)
    X,Y = np.meshgrid(x,y,indexing='ij')
    u =  np.sin(X) * np.cos(Y)
    v = -np.cos(X) * np.sin(Y)
    return u, v

def laplacian(u, dx, dy):
    return (np.roll(u,-1,0) - 2*u + np.roll(u,1,0))/dx**2 + (np.roll(u,-1,1) - 2*u + np.roll(u,1,1))/dy**2

def advect(u, v, dx, dy):
    du_dx = (np.roll(u,-1,0) - np.roll(u,1,0))/(2*dx)
    du_dy = (np.roll(u,-1,1) - np.roll(u,1,1))/(2*dy)
    dv_dx = (np.roll(v,-1,0) - np.roll(v,1,0))/(2*dx)
    dv_dy = (np.roll(v,-1,1) - np.roll(v,1,1))/(2*dy)
    adv_u = u*du_dx + v*du_dy
    adv_v = u*dv_dx + v*dv_dy
    return adv_u, adv_v

def pressure_projection(u, v, dx, dy):
    nx, ny = u.shape
    uhat = np.fft.rfftn(u); vhat = np.fft.rfftn(v)
    kx = 2*np.pi*np.fft.fftfreq(nx, d=dx)
    ky = 2*np.pi*np.fft.rffreq(ny, d=dy)
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    divhat = 1j*(KX*uhat + KY*vhat)
    denom = (KX**2 + KY**2); denom[0,0] = 1.0
    phat = divhat/denom
    uhat2 = uhat - 1j*KX*phat
    vhat2 = vhat - 1j*KY*phat
    u2 = np.fft.irfftn(uhat2, s=u.shape)
    v2 = np.fft.irfftn(vhat2, s=v.shape)
    return u2, v2

def cfl_dt(u, v, dx, dy, cfl=0.5, nu=1e-2):
    umax = max(np.max(np.abs(u)), np.max(np.abs(v)), 1e-8)
    adv = min(dx, dy)/umax
    diff = 0.25*min(dx,dy)**2/nu
    return cfl*min(adv, diff)

def energy_enstrophy(u, v, dx, dy):
    E = 0.5*np.mean(u*u + v*v)
    wx = (np.roll(v,-1,0)-np.roll(v,1,0))/(2*dx)
    wy = (np.roll(u,-1,1)-np.roll(u,1,1))/(2*dy)
    w = wy - wx
    Z = 0.5*np.mean(w*w)
    return E, Z

def run(args):
    outdir = os.path.abspath(args.outdir); os.makedirs(outdir, exist_ok=True)
    nx = ny = args.res
    L = 2*np.pi; dx = L/nx; dy = L/ny
    u, v = init_tg(nx, ny, L=L)
    nu = args.nu
    T = args.T; t = 0.0
    rows = []
    for step in range(args.steps):
        dt = cfl_dt(u, v, dx, dy, cfl=args.cfl, nu=nu)
        if t+dt > T: dt = T-t
        adv_u, adv_v = advect(u, v, dx, dy)
        u = u + dt*(-adv_u + nu*laplacian(u,dx,dy))
        v = v + dt*(-adv_v + nu*laplacian(v,dx,dy))
        u, v = pressure_projection(u, v, dx, dy)
        t += dt
        E, Z = energy_enstrophy(u, v, dx, dy)
        rows.append((t, E, Z, dt))
        if t >= T: break
    csv_path = os.path.join(outdir, "ns_timeseries.csv")
    with open(csv_path,"w",newline='',encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(["t","energy","enstrophy","dt"])
        for r in rows: w.writerow(r)
    ts = [r[0] for r in rows]; Es=[r[1] for r in rows]; Zs=[r[2] for r in rows]
    plt.figure(); plt.plot(ts,Es); plt.xlabel("t"); plt.ylabel("Energy"); plt.title("Energy decay"); plt.savefig(os.path.join(outdir,"energy.png"), dpi=160)
    plt.figure(); plt.plot(ts,Zs); plt.xlabel("t"); plt.ylabel("Enstrophy"); plt.title("Enstrophy"); plt.savefig(os.path.join(outdir,"enstrophy.png"), dpi=160)
    outs = [
        {"path":"ns_timeseries.csv","sha256":sha256_of_file(csv_path)},
        {"path":"energy.png","sha256":sha256_of_file(os.path.join(outdir,"energy.png"))},
        {"path":"enstrophy.png","sha256":sha256_of_file(os.path.join(outdir,"enstrophy.png"))},
    ]
    params = {"res":args.res,"nu":args.nu,"T":args.T,"steps":args.steps,"cfl":args.cfl}
    write_manifest(outdir, f"ns_full_{int(time.time())}", "NavierStokes", params, outs, notes="Taylor-Green vortex baseline")
    print("Navier-Stokes run complete:", outdir)

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", required=True)
    p.add_argument("--res", type=int, default=128)
    p.add_argument("--nu", type=float, default=1e-2)
    p.add_argument("--T", type=float, default=5.0)
    p.add_argument("--steps", type=int, default=2000)
    p.add_argument("--cfl", type=float, default=0.5)
    args = p.parse_args()
    run(args)
