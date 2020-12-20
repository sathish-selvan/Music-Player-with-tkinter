from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk 

root = Tk()
root.title("Mosic Player")
root.geometry("500x400")

#inti pygame mixer
pygame.mixer.init()

#grab song time info
global prevsong
prevsong = ''
def play_time():
    if stopped:
        return
    elif played:
        return
    current_time =int(pygame.mixer.music.get_pos()/1000)

    #temp label to get data
    
    
    #slider_val = time.strftime("%M:%S", time.gmtime(int(current_time)))
    #slider_label.config(text=slider_val)
    #slider_label.config(text=f'{int(my_slider.get())} and Song pos :{int(current_time)}')
    # my_slider.config(value=int(current_time))
    
    
    converted = time.strftime("%M:%S", time.gmtime(current_time))
    
    # finding the lngth of the mp3 usng mutagen
    global prevsong
    current_song = songs_box.curselection()
    song =  songs_box.get(current_song[0])
    prevsong = song
    song = f'C:/Users/Sathis/Desktop/my codes/tkinter folder/Music player with Tkinter/audio/{song}'
    song_mut = MP3(song)
    song_length = song_mut.info.length
    my_slider.config(to=song_length)
    converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))
    if int(my_slider.get()) == int(song_length):
        converted = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
        status_bar.config(text=f"Time Lapsed : {converted} of {converted_song_length}")
        pass
    elif paused:
        
        pass
    elif stopped:
        status_bar.config(text="")
        my_slider.config(value=0)
        pass
    elif int(my_slider.get())+1 == int(current_time):
        my_slider.config(value=int(current_time))
        #slider_label.config(text=f'{int(my_slider.get())} and Song pos :{int(current_time)}')
        status_bar.config(text=f"Time Lapsed : {converted} of {converted_song_length}")
    else:
        converted = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
        my_slider.config(value=int(my_slider.get()))
        #slider_label.config(text=f'{int(my_slider.get())} and Song pos :{int(current_time)}')
        status_bar.config(text=f"Time Lapsed : {converted} of {converted_song_length}")
        next_time = int(my_slider.get())+1
        my_slider.config(value=next_time)
    status_bar.after(1000,play_time)

#add song func
def add_song():
    song = filedialog.askopenfilename(initialdir ="audio/", title ="Choose a audio file", filetypes=(("mp3 Files", "*.mp3"), ))
    #strips the path
    song =  song.replace("C:/Users/Sathis/Desktop/my codes/tkinter folder/Music player with Tkinter/audio/","")
    songs_box.insert(END, song)
    songs_box.activate(0)
    songs_box.selection_set(0, last=None)

#Add many songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir ="audio/", title ="Choose a audio file", filetypes=(("mp3 Files", "*.mp3"), ))

    for song in songs:
        song =  song.replace("C:/Users/Sathis/Desktop/my codes/tkinter folder/Music player with Tkinter/audio/","")
        songs_box.insert(END, song)
    songs_box.activate(0)
    songs_box.selection_set(0, last=None)

#play a selected song
global played
played = False
global present_song
def play():
    
    global stopped
    stopped = False
    global present_song
    song = songs_box.get(ACTIVE)
    present_song = song
    global prev_song
    if prev_song == present_song:
        global played
        played = True
    else:
        
        played = False
    song = f'C:/Users/Sathis/Desktop/my codes/tkinter folder/Music player with Tkinter/audio/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Reset the slider attributes
    my_slider.config(value=0)
    #slider_label.config(text="00:00")
    play_time()
    
#stop func
global stopped
stopped = False
def stop():
    pygame.mixer.music.stop()
    #songs_box.selection_clear(ACTIVE)
    #clear the status bar
    status_bar.config(text="")
    #reset the slider attributes
    my_slider.config(value=0)
    #slider_label.config(text="00:00")
    global stopped
    stopped = True
#func for forward button
def next_song():
    try:
        global stopped
        stopped = False
        #GET the curent pos of the song
        next_one = songs_box.curselection()
        #Add 1 to move next pos of the song
        next_one = next_one[0]+1
        #now use the codes used in the play function
        song =  songs_box.get(next_one)
        song = f'C:/Users/Sathis/Desktop/my codes/tkinter folder/Music player with Tkinter/audio/{song}'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        #this clears the previous selection
        songs_box.selection_clear(0, END)
        #this adds the new section
        songs_box.activate(next_one)
        songs_box.selection_set(next_one, last=None)
        #reset the slider atributes
        my_slider.config(value=0)
        #lider_label.config(text="00:00")
       
    except:
        pass

def prev_song():
    try:
        global stopped
        stopped = False
        next_one = songs_box.curselection()
        next_one = next_one[0]-1
        song =  songs_box.get(next_one)
        song = f'C:/Users/Sathis/Desktop/my codes/tkinter folder/Music player with Tkinter/audio/{song}'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        songs_box.selection_clear(0, END)
        songs_box.activate(next_one)
        songs_box.selection_set(next_one, last=None)
        #Reset the slider attributes
        my_slider.config(value=0)
        #slider_label.config(text="00:00")
        stopped = False
    except:
        pass

#delete a song
def delete_song():
    stop()
    songs_box.delete(ANCHOR)
    pygame.mixer.music.stop()

#delete all songs
def delete_allsongs():
    stop()
    songs_box.delete(0,END)
    pygame.mixer.music.stop()

#global var to check the pause action
global paused
paused = False
# pause and unpause
def pause(is_paused):
    global paused
    paused = is_paused
    if not paused:
        pygame.mixer.music.pause()
        paused = True
    else:    
        pygame.mixer.music.unpause()
        paused = False

def slide(x):
    # slider_val = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
    # slider_label.config(text=slider_val)

    song = songs_box.get(ACTIVE)
    song = f'C:/Users/Sathis/Desktop/my codes/tkinter folder/Music player with Tkinter/audio/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start =int(my_slider.get()))
    #pygame.mixer.music.set_pos(int(my_slider.get())*1000)

#playlist box
songs_box = Listbox(root,bg="black",fg="green", width=60, selectbackground="gray", selectforeground="black")
songs_box.pack(pady=20)

#images for controls
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img =PhotoImage(file='images/forward.png')
play_btn_img =PhotoImage(file='images/play.png')
stop_btn_img =PhotoImage(file='images/stop.png')
pause_btn_img =PhotoImage(file='images/pause.png')

#frames for controls
controls_frame = Frame(root)
controls_frame.pack()

#controls buttons
back_button = Button(controls_frame, image = back_btn_img, borderwidth=0, command =  prev_song)
forward_button = Button(controls_frame, image = forward_btn_img, borderwidth=0, command = next_song)
play_button=Button(controls_frame, image = play_btn_img, borderwidth=0, command = play)
stop_button=Button(controls_frame, image = stop_btn_img, borderwidth=0, command = stop)
pause_button = Button(controls_frame, image = pause_btn_img, borderwidth=0, command=lambda: pause(paused))

back_button.grid(row=0 , column=0, padx=10)
forward_button.grid(row=0 , column=1, padx=10) 
play_button.grid(row=0 , column=2, padx=10)
stop_button.grid(row=0 , column=3, padx=10)
pause_button.grid(row=0 , column=4, padx=10)

#menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add_songs
add_songs_menu= Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu = add_songs_menu)
add_songs_menu.add_command(label="Add one song to the playlist", command=add_song)
#add many songs
add_songs_menu.add_command(label="Add many song to the playlist", command=add_many_songs)
#menu for remove a song
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu = remove_song_menu)
remove_song_menu.add_command(label="Delete a song from the play list", command =  delete_song)
remove_song_menu.add_command(label="Delete all songs from the play list", command = delete_allsongs)

#statusbar
status_bar = Label(root, text="", bd=1, relief = GROOVE, anchor = E)
status_bar.pack(fill=X, side= BOTTOM, ipady=2)

#music pos slider
my_slider = ttk.Scale(root,from_=0, to=100, orient=HORIZONTAL, value=0,length=360, command=slide)
my_slider.pack(pady=20)

#slider label
#slider_label = Label(root,text = "00:00")
#lider_label.pack(pady=10)
root.mainloop()