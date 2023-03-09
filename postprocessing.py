import adelio            as aio
import matplotlib.pyplot as plt
import numpy             as np
import os
import preprocessing     as pre
import processing        as pro


def analyse_single_experience(path: str) -> None:
    
    # Parameters of the figure
    ncols = 7
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

    # Horizontal and vertical profiles
    axe = fig.add_subplot(1, ncols, 5)
    axe.plot(
        np.linspace(0, N-1, N),
        auto[:, N//2]
    )
    axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
    axe.set_title("Vertical profile")

    axe = fig.add_subplot(1, ncols, 6)
    axe.plot(
        np.linspace(0, N-1, N),
        auto[N//2, :]
    )
    axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
    axe.set_title("Horizontal profile")

    plt.savefig(f"{os.path.basename(path)}_analysis.jpg")
    plt.close()

    return None



def analyse_folder_experiences(path: str) -> None:
    experience_names = os.listdir(path)

    nrows = len(experience_names)
    ncols = 7
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

        # Horizontal and vertical profiles
        axe = fig.add_subplot(nrows, ncols, n*ncols+5)
        axe.plot(
            np.linspace(0, N-1, N),
            auto[:, N//2]
        )
        axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
        axe.set_title("Vertical profile")

        axe = fig.add_subplot(nrows, ncols, n*ncols+6)
        axe.plot(
            np.linspace(0, N-1, N),
            auto[N//2, :]
        )
        axe.hlines(y=cinf, xmin=axe.get_xlim()[0], xmax=axe.get_xlim()[1])
        axe.set_title("Horizontal profile")

    plt.savefig(f"{os.path.basename(path)}_analysis.jpg")
    plt.close()

    return None
