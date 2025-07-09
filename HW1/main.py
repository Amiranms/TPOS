import libtmux
import os
import click
import shutil
from uuid import uuid4


BASE_PORT = 322
WORKING_DIR = 'main_dir'
MAIN_SESSION_NAME = 'main_session'

def start(num_users, base_dir = '.'):
    """
    Запустить $num окружений. У каждого рабочая директория $base_dir/+$dir + $i
    """
    ports = list(range(BASE_PORT, BASE_PORT + num_users))
    main_dir = os.path.join(base_dir, WORKING_DIR)
    os.makedirs(main_dir, exist_ok=True)
    os.chdir(main_dir)

    # 1 сервер, 1 сессия для всех окружений
    server = libtmux.Server()

    session = server.new_session(MAIN_SESSION_NAME, kill_session=True, window_name="main_window")

    for num in range(num_users):
        dir_name = f"dir{num}"
        os.makedirs(dir_name, exist_ok=True)
        os.chdir(dir_name)
        token = uuid4()
        window = session.new_window("window_" + str(num))
        pane = window.attached_pane
        pane.send_keys(f"jupyter notebook --ip 0.0.0.0 --port {ports[num]} --no-browser "
                       f"--NotebookApp.token={token} --NotebookApp.notebook_dir='./'", enter=True)
        print(f"id:<{num}>, port:<{ports[num]}>, token:<{token}>")
        os.chdir("..")

    main_window = next((w for w in session.windows if w.name == "main_window"), None)
    if main_window:
        main_window.kill_window()

def stop(num):
    """
        num: номер окружения, которое необходимо остановить
    """
    server = libtmux.Server()
    session = next((s for s in server.sessions if s.name == 'main_session'), None)
    if not session:
        print("Session not found.")
        return

    # Найти и удалить директорию окружения, затем остановить окно
    window = next((w for w in session.windows if w.name == f"window_{num}"), None)
    if window:
        init_path = window.attached_pane.pane_start_path
        if init_path.endswith(f"dir{num}"):
            shutil.rmtree(init_path, ignore_errors=True)
            window.kill_window()


def stop_all():
    server = libtmux.Server()
    session = next((s for s in server.sessions if s.name == 'main_session'), None)
    if session:
        session.kill_session()
    shutil.rmtree(WORKING_DIR, ignore_errors=True)

@click.command()
@click.argument('func')
@click.argument('num', default=1, type=click.INT)
def dispatcher(func, num):
    if func == 'start':
        start(num)
    elif func == 'stop':
        stop(num)
    elif func == 'stop_all':
        stop_all()
    else:
        print('wrong parameters')




if __name__ == '__main__':
    dispatcher()
