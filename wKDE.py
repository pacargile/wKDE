def dokde(inarr,wgt=None):
        # parse inarr to just those values with wgt > 1e-5
        cond = wgt >= 1e-5
        inarr_i = inarr[cond]
        wgt = wgt[cond]
        xeval = np.linspace(inarr_i.min(),inarr_i.max(),1000)
        kde = KDEUnivariate(inarr_i)
        kde.fit(weights=wgt,fft=False)
        yeval = kde.evaluate(xeval)
        return xeval,yeval

def genkde(intab):
        inwgt = np.exp(intab['logwt']-intab['logz'][-1])
        outdict = {}
        for par in pararr:
                intab_i = intab[par]
                inKDE = dokde(intab_i,wgt=inwgt)
                outdict[par] = inKDE
        return outdict

def genstat(kde):
        maxval = kde[0][np.argmax(kde[1])]
        normkde = kde[1] / kde[1].sum()
        kdeval_16 = kde[0][np.argmin(np.abs(normkde.cumsum()-0.16))]
        kdeval_84 = kde[0][np.argmin(np.abs(normkde.cumsum()-0.84))]
        ul = kdeval_84 - maxval
        ll = maxval - kdeval_16
        return maxval,ul,ll
