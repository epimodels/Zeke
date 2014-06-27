from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from .models import ZombieSIR
from .models import ZombieSEIR
from .models import Haven
from .models import SlowSIR
import cStringIO


try:
    # Python 3
    from urllib.parse import parse_qs
except:
    # Python 2
    from urlparse import parse_qs


# XXX Quick and dirty options selector
OPTIONS = """
                <option value="sir"%s>SIR</option>
                <option value="seir"%s>SEIR</option>
                <option value="haven"%s>Haven</option>
                <option value="slowsir"%s>SlowSIR</option>
"""


PSI, BETA, BETA_F, BETA_H, GAMMA, ALPHA, KAPPA = (
    0.07, 0.5, 0.5, 0.25, 0.1, 0.5, 0.05)


def about(request):
    return render(request, "about.html", {})


def contact(request):
    return render(request, "contact.html", {})


def error():
    """
    """
    # http://matplotlib.org/examples/pylab_examples/demo_annotation_box.html
    from matplotlib._png import read_png
    from matplotlib.cbook import get_sample_data
    from matplotlib.offsetbox import OffsetImage
    from matplotlib.offsetbox import AnnotationBbox
    import os
    fn = get_sample_data(os.path.join(
                         os.path.dirname(__file__),
                         "static",
                         "white-background.png"),
                         asfileobj=False)
    image = read_png(fn)
    imagebox = OffsetImage(image)
    xy = (0.5, 0.5)
    ab = AnnotationBbox(imagebox, xy)
    return ab


def _login(request):
    username = None
    password = None
    if 'username' in request.POST:
        username = request.POST['username']
    if 'password' in request.POST:
        password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/")
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        pass
    return render(request, "login.html", {})


def _logout(request):
    """
    """
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


def root(request):
    query_string = request.META['QUERY_STRING']
    qs = parse_qs(query_string)

    # XXX Quick and dirty options selector
    options = (' selected', '', '', '')
    model = 'sir'

    psi, beta, beta_f, beta_h, gamma, alpha, kappa = (
        PSI, BETA, BETA_F, BETA_H, GAMMA, ALPHA, KAPPA)

    if 'model' in qs:
        selected = qs['model']

        if 'reset' in qs:
            qs = {}
            qs['model'] = selected
            query_string = 'model=%s' % selected[0]

        # XXX Quick and dirty options selector
        if 'sir' in selected:
            options = (' selected', '', '', '')
            model = 'sir'
        if 'seir' in selected:
            options = ('', ' selected', '', '')
            model = 'seir'
        if 'haven' in selected:
            # Fix defaults
            gamma = 0.10
            alpha = 0.50
            options = ('', '', ' selected', '')
            model = 'haven'
        if 'slowsir' in selected:
            options = ('', '', '', ' selected')
            model = 'slowsir'

    # Persist qs values across page loads
    if 'psi' in qs:
        psi = float(qs['psi'][0])
    if 'beta' in qs:
        beta = float(qs['beta'][0])
    if 'beta_f' in qs:
        beta_f = float(qs['beta_f'][0])
    if 'beta_h' in qs:
        beta_h = float(qs['beta_h'][0])
    if 'gamma' in qs:
        gamma = float(qs['gamma'][0])
    if 'alpha' in qs:
        alpha = float(qs['alpha'][0])
    if 'kappa' in qs:
        kappa = float(qs['kappa'][0])

    return render(request, "root.html", {
        'project': 'hai_pyramid',
        'query_string': query_string,
        'options': OPTIONS % options,
        'model': model,
        'psi': psi,
        'beta': beta,
        'beta_f': beta_f,
        'beta_h': beta_h,
        'gamma': gamma,
        'alpha': alpha,
        'kappa': kappa,
        'user': request.user,
    })


def plot(request):
    """
    http://stackoverflow.com/a/5515994/185820
    """
    query_string = request.META['QUERY_STRING']
    qs = parse_qs(query_string)

    psi, beta, beta_f, beta_h, gamma, alpha, kappa = (
        PSI, BETA, BETA_F, BETA_H, GAMMA, ALPHA, KAPPA)

    if 'model' in qs:

        if 'sir' in qs['model']:
            if 'beta' in qs:
                beta = float(qs['beta'][0])
            if 'gamma' in qs:
                gamma = float(qs['gamma'][0])
            canvas = plot_sir(beta, gamma)

        if 'seir' in qs['model']:
            if 'beta' in qs:
                beta = float(qs['beta'][0])
            if 'gamma' in qs:
                gamma = float(qs['gamma'][0])
            if 'alpha' in qs:
                alpha = float(qs['alpha'][0])
            canvas = plot_seir(beta, gamma, alpha)

        if 'haven' in qs['model']:
            # Fix defaults
            gamma = 0.10
            alpha = 0.50
            if 'psi' in qs:
                psi = float(qs['psi'][0])
            if 'beta_f' in qs:
                beta_f = float(qs['beta_f'][0])
            if 'beta_h' in qs:
                beta_h = float(qs['beta_h'][0])
            if 'gamma' in qs:
                gamma = float(qs['gamma'][0])
            if 'alpha' in qs:
                alpha = float(qs['alpha'][0])
            if 'kappa' in qs:
                kappa = float(qs['kappa'][0])
            canvas = plot_haven(beta_f, beta_h, gamma, alpha, kappa, psi)

        if 'slowsir' in qs['model']:
            if 'beta' in qs:
                beta = float(qs['beta'][0])
            if 'gamma' in qs:
                gamma = float(qs['gamma'][0])
            canvas = plot_slowsir(beta, gamma)
    else:
        canvas = plot_sir(beta, gamma)

    # write image data to a string buffer and get the PNG image bytes
    buf = cStringIO.StringIO()
    canvas.print_png(buf)
    data = buf.getvalue()

    # write image bytes back to the browser
    return HttpResponse(data, content_type="image/png")


def plot_sir(infect_prob, infect_duration):
    """
    Plot SIR, return canvas
    """
    sir = ZombieSIR(infect_prob, infect_duration)
    figure = Figure()
    canvas = FigureCanvasAgg(figure)
    axes = figure.add_subplot(1, 1, 1)

    if sir is not False:
        axes.plot(sir[0], sir[1], 'g--', linewidth=3)
        axes.plot(sir[0], sir[2], 'r-', linewidth=3)
        axes.plot(sir[0], sir[3], '-.b', linewidth=3)
        axes.set_xlabel("Time (days)")
        axes.set_ylabel("Percent of Population")
        axes.set_title("Zombie SIR Epidemic\n(R_0: %s)" % sir[4])
        axes.grid(True)
        axes.legend(("Survivors", "Zombies", "Dead"),
                    shadow=True, fancybox=True)
    else:
        ab = error()
        axes.set_title("Sorry, there has been an error.")
        axes.add_artist(ab)

    return canvas


def plot_seir(infect_prob, infect_duration, latent_period):
    """
    Plot SEIR, return canvas
    """
    seir = ZombieSEIR(infect_prob, infect_duration, latent_period)
    figure = Figure()
    canvas = FigureCanvasAgg(figure)
    axes = figure.add_subplot(1, 1, 1)

    if seir is not False:
        axes.plot(seir[0], seir[1], 'g--', linewidth=3)
        axes.plot(seir[0], seir[2], ':m', linewidth=3)
        axes.plot(seir[0], seir[3], 'r-', linewidth=3)
        axes.plot(seir[0], seir[4], '-.b', linewidth=3)
        axes.set_xlabel("Time (days)")
        axes.set_ylabel("Percent of Population")
        axes.set_title("Zombie SEIR Epidemic")
        axes.grid(True)
        axes.legend(
            ("Survivors", "Latent", "Zombies", "Dead"),
            shadow=True, fancybox=True)
    else:
        ab = error()
        axes.set_title("Sorry, there has been an error.")
        axes.add_artist(ab)

    return canvas


def plot_haven(infect_prob_free, infect_prob_safe, infect_duration,
               latent_period, kill_prob, time_to_shelter):
    """
    Plot Haven, return canvas
    """
    haven = Haven(
        infect_prob_free, infect_prob_safe, infect_duration,
        latent_period, kill_prob, time_to_shelter)
    figure = Figure()
    canvas = FigureCanvasAgg(figure)
    axes = figure.add_subplot(2, 1, 1)
    if haven is not False:
        axes.plot(haven[0], haven[1], 'g--', linewidth=3)
        axes.plot(haven[0], haven[2], '-.b', linewidth=3)
        axes.plot(haven[0], haven[3], ':m', linewidth=3)
        axes.plot(haven[0], haven[4], 'r-', linewidth=3)
        axes.set_xlabel("Time (days)")
        axes.set_ylabel("Percent of Population")
        axes.set_title("Safe Haven Results - Low Kappa")
        axes.grid(True)
        axes.legend(
            ("Wandering", "Safe Survivors", "Latent", "Infected"), shadow=True,
            fancybox=True)
        axes = figure.add_subplot(2, 1, 2)
        axes.plot(haven[0], haven[5], 'k--', linewidth=3)
        axes.plot(haven[0], haven[6], '-.b', linewidth=3)
        axes.set_xlabel("Time (days)")
        axes.set_ylabel("Percent of Population")
        axes.grid(True)
        axes.legend(("Culled", "Dead"), shadow=True, fancybox=True)
    else:
        ab = error()
        axes.set_title("Sorry, there has been an error.")
        axes.add_artist(ab)
    return canvas


def plot_slowsir(infect_prob, infect_duration):

    """
    Plot SIR slowly, return canvas
    """
    slowsir = SlowSIR(infect_prob, infect_duration)
    figure = Figure()
    canvas = FigureCanvasAgg(figure)
    axes = figure.add_subplot(1, 1, 1)

    if slowsir is not False:
        axes.plot(slowsir[0], slowsir[1], 'g--', linewidth=3)
        axes.plot(slowsir[0], slowsir[2], 'r-', linewidth=3)
        axes.plot(slowsir[0], slowsir[3], '-.b', linewidth=3)
        axes.set_xlabel("Time (days)")
        axes.set_ylabel("Percent of Population")
        axes.set_title("Zombie SIR Epidemic")
        axes.grid(True)
        axes.legend(("Survivors", "Zombies", "Dead"),
                    shadow=True, fancybox=True)
    else:
        ab = error()
        axes.set_title("Sorry, there has been an error.")
        axes.add_artist(ab)
    return canvas
