from email import header
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from matplotlib import pyplot as plt

website = "https://blaze.com/en/games/double?modal=double_history_index"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 

def plot_results(color_list):
    num_of_color = {"red": 0, "black": 0, "white": 0}
    for element in color_list:
        if element == "red":
            num_of_color["red"] += 1
        if element == "black":
            num_of_color["black"] += 1
        if element == "white":
            num_of_color["white"] += 1


    plt.style.use("fivethirtyeight")
    total_colors_picked = len(color_list)
    for i in range(2):
        if list(num_of_color.values())[i]/total_colors_picked > 0.5:
            plt.bar(list(num_of_color.keys())[i], list(num_of_color.values())[i], color = 'g')
        elif list(num_of_color.values())[i]/total_colors_picked < 0.5:
            plt.bar(list(num_of_color.keys())[i], list(num_of_color.values())[i], color = 'r')
        else:
            plt.bar(list(num_of_color.keys())[i], list(num_of_color.values())[i], color = 'b')

    if list(num_of_color.values())[2]/total_colors_picked > (1/14):
        plt.bar(list(num_of_color.keys())[2], list(num_of_color.values())[2], color = 'g')
    elif list(num_of_color.values())[2]/total_colors_picked < 0.5:
        plt.bar(list(num_of_color.keys())[2], list(num_of_color.values())[2], color = 'r')
    else:
        plt.bar(list(num_of_color.keys())[2], list(num_of_color.values())[2], color = 'b')


    plt.ylabel("quantity selected")
    plt.xlabel("total_colors_picked = {} " .format(total_colors_picked))
    plt.title("Blaze Double results")
    plt.show()


def play_double(color_list):
    
    print("how much money do you want to play with?")
    your_money = int(input())

    for i in range(len(color_list)):

        if your_money == 0:
            break

        print("pick a color (red, black or white)")
        chosen_color = input()

        print("place a bet")
        bet = int(input())
        print("\n")

        while bet > your_money:
            print("insufficient funds, try again")
            print("place a bet")
            bet = int(input())
            print("\n")

        if chosen_color == "white":
            if color_list[i] == chosen_color:
                print("the winning color is " + color_list[i])
                print("well done!")
                your_money += bet*13
                print("now you have {} dollars\n\n" .format(your_money))
            else:
                print("the winning color is " + color_list[i])
                print("better luck next time")
                your_money -= bet
                print("now you have {} dollars\n\n" .format(your_money))
        else:
            if str(color_list[i]) == chosen_color:
                print("the winning color is " + color_list[i])
                print("well done!")
                your_money += bet
                print("now you have {} dollars\n\n" .format(your_money))
            else:
                print("the winning color is " + color_list[i])
                print("better luck next time")
                your_money -= bet
                print("now you have {} dollars\n\n" .format(your_money))

    print("now you have {} dollars" .format(your_money))

def write_to_csv(dictionary):
    df = pd.DataFrame.from_dict(dictionary, orient='index')
    df.to_csv('selected_colors.csv', index=False)

dictionary = {}
number_of_times = 1
for round in range(number_of_times):
    driver.get(website)
    time.sleep(1)

    selected_seeds = driver.find_elements(By.XPATH, ".//tbody/tr/td[3]/div/a")
    selected_colors = driver.find_elements(By.XPATH, ".//tbody/tr/td[2]/div/div")

    for i in range(9,-1, -1):
        seed = selected_seeds[i].text
        trash, color = selected_colors[i].get_attribute('class').split(" ")

        if seed not in dictionary:
            dictionary[seed] = color


    if round != number_of_times - 1:
        time.sleep(20)


write_to_csv(dictionary)

color_list = []
for i in dictionary:
    color_list.append(dictionary[i])
color_list.reverse()

plot_results(color_list)

play_double(color_list)

driver.quit()
