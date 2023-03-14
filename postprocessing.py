import adelio            as aio
import matplotlib.pyplot as plt
import numpy             as np
import os
import preprocessing     as pre
import processing        as pro

def analyse_single(path: str) -> None:
    
    # Parameters of the figure
    ncols = 6
    size  = 10
    fig   = plt.figure(figsize=(ncols*size+1, 1*size))

    # Discretisation of the interval [0, PI], then [0, 2*PI]
    angles = np.linspace(0, np.pi, 256)
    angles_ = np.hstack((angles, np.pi+angles))

    # Preprocess the data
    field = pre.exp2pic(path)
    N     = field.shape[0]

    # Compute the autocorrelation and C_inf
    auto = pro.autocorrelation(field)
    cinf = pro.cinf(field)

    # Plot the field
    axe = fig.add_subplot(1, ncols, 1)
    axe.imshow(field, cmap="hot")
    axe.contour(field, [cinf, 1])
    axe.set_xlabel("x [px]")
    axe.set_ylabel("y [px]")
    axe.set_title(f"{os.path.basename(path)} --- "+"$E_{yy}$")

    # Plot the autocorrelation with the contour of C_inf
    axe = fig.add_subplot(1, ncols, 2)
    axe.imshow(auto)
    axe.contour(auto, [cinf, 1])
    axe.set_xlabel("x [px]")
    axe.set_ylabel("y [px]")
    axe.set_title("$\mathcal{A}(E_{yy})$ ; $C_\infty=$"+"{:.3f}".format(cinf))

    # Compute the length versus the angle : L(angle) then polar plot
    length = np.zeros_like(angles)
    for i in range(length.shape[0]):
        length[i] = pro.length_vs_angle(auto, cinf, angles[i])
    
    width = pro.length_vs_angle(auto, cinf, angles[length.argmax()]+np.pi/2)
    
    length_ = np.hstack((length, length))

    axe = fig.add_subplot(1, ncols, 3)
    axe.plot(angles*180/np.pi, length)
    axe.set_xlabel("angle [°]")
    axe.set_ylabel("length [px]")
    axe.set_title("Max : $\\theta=$"+"{:.2f}".format(angles[length.argmax()]*180/np.pi)+"° ; $R(\\theta) =$"+"{:.2f}".format(length.max())+"[px] ; $W(\\theta) =$"+"{:.3f}".format(width)+"[px]")

    axe = fig.add_subplot(1, ncols, 4, projection="polar")
    axe.fill(angles_, length_, color="tan")
    axe.set_rmax(length.max())

    # Vertical profile
    axe = fig.add_subplot(1, ncols, 5)
    axe.plot(
        np.linspace(0, N-1, N),
        auto[:, N//2]
    )
    axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
    axe.set_title("Vertical profile")

    # Radial profile in the min length direction
    r, v = pro.radial_profile(field, angles[length.argmax()]+np.pi/2)
    axe  = fig.add_subplot(1, ncols, 6)
    axe.plot(r, v)
    axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
    axe.set_xlabel("Radius [px]")
    axe.set_ylabel("$\\mathcal{A}(E_{yy})$")
    axe.set_title("Radial for $\\theta = $"+"{:.3f}".format((angles[length.argmax()]+np.pi/2)/np.pi*180)+"°")
    
    plt.savefig(f"out/{os.path.basename(path)}_analysis.jpg")
    plt.close()

    return None



def analyse_folder(path: str) -> None:
    experience_names = os.listdir(path)

    nrows = len(experience_names)
    ncols = 6
    size  = 10
    fig   = plt.figure(figsize=(ncols*size+1, nrows*size))

    angles = np.linspace(0, np.pi, 256)
    angles_ = np.hstack((angles, np.pi+angles))

    for n, experience_name in enumerate(experience_names):

        path_ = os.path.join(path, experience_name)
        field = pre.exp2pic(path_)
        N     = field.shape[0]

        # Compute the autocorrelation and C_inf
        auto = pro.autocorrelation(field)
        cinf = pro.cinf(field)

        # Plot the field
        axe = fig.add_subplot(nrows, ncols, n*ncols+1)
        axe.imshow(field, cmap="hot")
        axe.contour(field, [cinf, 1])
        axe.set_xlabel("x [px]")
        axe.set_ylabel("y [px]")
        axe.set_title(f"{experience_name} --- "+"$E_{yy}$")

        # Plot the autocorrelation with the contour of C_inf
        axe = fig.add_subplot(nrows, ncols, n*ncols+2)
        axe.imshow(auto)
        axe.contour(auto, [cinf, 1])
        axe.set_xlabel("x [px]")
        axe.set_ylabel("y [px]")
        axe.set_title("$\mathcal{A}(E_{yy})$ ; $C_\infty=$"+"{:.3f}".format(cinf))

        # Compute the length versus the angle : L(angle) then polar plot
        length = np.zeros_like(angles)
        for i in range(length.shape[0]):
            length[i] = pro.length_vs_angle(auto, cinf, angles[i])
        
        width = pro.length_vs_angle(auto, cinf, angles[length.argmax()]+np.pi/2)
        
        length_ = np.hstack((length, length))

        axe = fig.add_subplot(nrows, ncols, n*ncols+3)
        axe.plot(angles*180/np.pi, length)
        axe.set_xlabel("angle [°]")
        axe.set_ylabel("length [px]")
        axe.set_title("Max : $\\theta=$"+"{:.2f}".format(angles[length.argmax()]*180/np.pi)+"° ; $R(\\theta) =$"+"{:.2f}".format(length.max())+"[px] ; $W(\\theta) =$"+"{:.3f}".format(width)+"[px]")

        axe = fig.add_subplot(nrows, ncols, n*ncols+4, projection="polar")
        axe.fill(angles_, length_, color="tan")
        axe.set_rmax(length.max())

        # Vertical profile
        axe = fig.add_subplot(nrows, ncols, n*ncols+5)
        axe.plot(
            np.linspace(0, N-1, N),
            auto[:, N//2]
        )
        axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
        axe.set_title("Vertical profile")

        # Radial profile in the direction of the minimum length
        r, v = pro.radial_profile(field, angles[length.argmax()]+np.pi/2)

        axe = fig.add_subplot(nrows, ncols, n*ncols+6)
        axe.plot(r, v)
        axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
        axe.set_xlabel("Radius [px]")
        axe.set_ylabel("$\\mathcal{A}(E_{yy})$")
        axe.set_title("Radial for $\\theta = $"+"{:.3f}".format((angles[length.argmax()]+np.pi/2)/np.pi*180)+"°")

    plt.savefig(f"out/{os.path.basename(path)}_analysis.jpg")
    plt.close()

    return None



def analyse_simulation(path: str) -> None:

    # Get the Pfile
    ppath = os.path.join(path, "".join([filename for filename in os.listdir(path) if filename.startswith("p")]))
    pfile = aio.Pfile(ppath)

    # Get the available dates
    tpath = os.path.join(path, "".join([filename for filename in os.listdir(path) if filename.startswith("t")]))
    tfile = aio.Tfile(tpath)
    dates = tfile.read()

    # Iterate over date indices
    for tn in range(len(dates)):

        if tn > 0:
            # Iterate over tensor fields
            for name in ['d', 'e', 's']:

                # Preprocess the field
                field = pre.field2pic(pfile, name, tn)[1]
                N     = field.shape[0]

                # Parameters of the figure
                ncols = 6
                size  = 10
                fig   = plt.figure(figsize=(ncols*size+1, 1*size))

                # Discretisation of the interval [0, PI], then [0, 2*PI]
                angles = np.linspace(0, np.pi, 256)
                angles_ = np.hstack((angles, np.pi+angles))

                # Compute the autocorrelation and C_inf
                auto = pro.autocorrelation(field)
                cinf = pro.cinf(field)

                # Plot the field
                axe = fig.add_subplot(1, ncols, 1)
                axe.imshow(field, cmap="hot")
                axe.contour(field, [cinf, 1])
                axe.set_xlabel("x [px]")
                axe.set_ylabel("y [px]")
                axe.set_title(f"{os.path.basename(path)} --- J2({name})")

                # Plot the autocorrelation with the contour of C_inf
                axe = fig.add_subplot(1, ncols, 2)
                axe.imshow(auto)
                axe.contour(auto, [cinf, 1])
                axe.set_xlabel("x [px]")
                axe.set_ylabel("y [px]")
                axe.set_title("$\mathcal{A}$ ; $C_\infty=$"+"{:.3f}".format(cinf))

                # Compute the length versus the angle : L(angle) then polar plot
                length = np.zeros_like(angles)
                for i in range(length.shape[0]):
                    length[i] = pro.length_vs_angle(auto, cinf, angles[i])
                
                width = pro.length_vs_angle(auto, cinf, angles[length.argmax()]+np.pi/2)
                
                length_ = np.hstack((length, length))

                axe = fig.add_subplot(1, ncols, 3)
                axe.plot(angles*180/np.pi, length)
                axe.set_xlabel("angle [°]")
                axe.set_ylabel("length [px]")
                axe.set_title("Max : $\\theta=$"+"{:.2f}".format(angles[length.argmax()]*180/np.pi)+"° ; $R(\\theta) =$"+"{:.2f}".format(length.max())+"[px] ; $W(\\theta) =$"+"{:.3f}".format(width)+"[px]")

                axe = fig.add_subplot(1, ncols, 4, projection="polar")
                axe.fill(angles_, length_, color="tan")
                axe.set_rmax(length.max())

                # Radial profile in the min length direction
                r, v = pro.radial_profile(field, angles[length.argmax()]+np.pi/2)
                axe  = fig.add_subplot(1, ncols, 5)
                axe.plot(r, v)
                axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
                axe.set_xlabel("Radius [px]")
                axe.set_ylabel("$\\mathcal{A}(E_{yy})$")
                axe.set_title("Radial for $\\theta = $"+"{:.3f}".format((angles[length.argmax()]+np.pi/2)/np.pi*180)+"°")
                
                fft_auto = np.abs(np.fft.fft2(auto))
                axe = fig.add_subplot(1, ncols, 6)
                axe.imshow(fft_auto)
                axe.set_xlabel("freq. [Hz]")
                axe.set_ylabel("freq. [Hz]")
                axe.set_title("$|\mathcal{F}\left(\mathcal{A}(J2)\\right)|$")

                plt.savefig(f"out/J2{name}_{tn}_analysis.jpg")
                plt.close()


        # Preprocess Peierls
        peierls = pre.peierls2pic(pfile, tn)
        N       = peierls.shape[0]

        # Parameters of the figure
        ncols = 6
        size  = 10
        fig   = plt.figure(figsize=(ncols*size+1, 1*size))

        # Discretisation of the interval [0, PI], then [0, 2*PI]
        angles = np.linspace(0, np.pi, 256)
        angles_ = np.hstack((angles, np.pi+angles))

        # Compute the autocorrelation and C_inf
        auto = pro.autocorrelation(peierls)
        cinf = pro.cinf(peierls)

        # Plot the field
        axe = fig.add_subplot(1, ncols, 1)
        axe.imshow(peierls, cmap="hot")
        axe.contour(peierls, [cinf, 1])
        axe.set_xlabel("x [px]")
        axe.set_ylabel("y [px]")
        axe.set_title(f"{os.path.basename(path)} --- "+"Peierls")

        # Plot the autocorrelation with the contour of C_inf
        axe = fig.add_subplot(1, ncols, 2)
        axe.imshow(auto)
        axe.contour(auto, [cinf, 1])
        axe.set_xlabel("x [px]")
        axe.set_ylabel("y [px]")
        axe.set_title("$\mathcal{A}(Peierls)$ ; $C_\infty=$"+"{:.3f}".format(cinf))

        # Compute the length versus the angle : L(angle) then polar plot
        length = np.zeros_like(angles)
        for i in range(length.shape[0]):
            length[i] = pro.length_vs_angle(auto, cinf, angles[i])
        
        width = pro.length_vs_angle(auto, cinf, angles[length.argmax()]+np.pi/2)
        
        length_ = np.hstack((length, length))

        axe = fig.add_subplot(1, ncols, 3)
        axe.plot(angles*180/np.pi, length)
        axe.set_xlabel("angle [°]")
        axe.set_ylabel("length [px]")
        axe.set_title("Max : $\\theta=$"+"{:.2f}".format(angles[length.argmax()]*180/np.pi)+"° ; $R(\\theta) =$"+"{:.2f}".format(length.max())+"[px] ; $W(\\theta) =$"+"{:.3f}".format(width)+"[px]")

        axe = fig.add_subplot(1, ncols, 4, projection="polar")
        axe.fill(angles_, length_, color="tan")
        axe.set_rmax(length.max())

        # Radial profile in the min length direction
        r, v = pro.radial_profile(peierls, angles[length.argmax()]+np.pi/2)
        axe  = fig.add_subplot(1, ncols, 5)
        axe.plot(r, v)
        axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
        axe.set_xlabel("Radius [px]")
        axe.set_ylabel("$\\mathcal{A}(E_{yy})$")
        axe.set_title("Radial for $\\theta = $"+"{:.3f}".format((angles[length.argmax()]+np.pi/2)/np.pi*180)+"°")

        freq = np.abs(np.fft.fftshift(np.abs(np.fft.fft2(np.fliplr(peierls)))))
        axe = fig.add_subplot(1, ncols, 6)
        axe.imshow(freq)
        axe.set_xlim()
        axe.set_xlabel("freq. [Hz]")
        axe.set_ylabel("freq. [Hz]")
        axe.set_title("$|\mathcal{F}(Peierls)|$")
        
        plt.savefig(f"out/peierls_{tn}_analysis.jpg")
        plt.close()

    return None
