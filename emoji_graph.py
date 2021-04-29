# FILE FOR CREATING EMOJI-ACCURACY GRAPHS. CAN ONLY BE RUN ON MACOS.

#function to create a scatterplot with emojis as markers
#based on https://towardsdatascience.com/how-i-got-matplotlib-to-plot-apple-color-emojis-c983767b39e0
#follow instructions above to install & build mplcairo

#Set the backend to use mplcairo
import matplotlib, mplcairo
print('Default backend: ' + matplotlib.get_backend())
matplotlib.use("module://mplcairo.macosx")
print('Backend is now ' + matplotlib.get_backend())

# IMPORTANT: Import these libraries only AFTER setting the backend
import matplotlib.pyplot as plt, numpy as np
from matplotlib.font_manager import FontProperties
class Emoji_Graph:
    def __init__(self):
        emojis = {
            0: '❤',
            1: '😍',
            2: '😂',
            3: '💕',
            4: '🔥',
            5: '😊',
            6: '😎',
            7: '✨',
            8: '💙',
            9: '😘',
            10: '📷',
            11: '🇺🇸',
            12: '☀',
            13: '💜',
            14: '😉',
            15: '💯',
            16: '😁',
            17: '🎄',
            18: '📸',
            19: '😜'
        }
        # Load Apple Color Emoji font
        self.prop = FontProperties(fname='/System/Library/Fonts/Apple Color Emoji.ttc')
        self.emoji_array = [e for e in emojis.values()]
        self.x_datasize = [10760, 5279, 5241, 2885, 2517, 2317, 2049, 1894, 1796, 1671, 1544, 1528, 1462, 1346, 1377, 1249, 1306, 1279, 1286, 1214]
    def plot(self, y_acc, title, savename = None, emojis=None, emojis_occ=None):
        if emojis:
            self.emoji_array = self.emoji_array = [e for e in emojis.values()]
            self.x_datasize = emojis_occ
        # set up the plot
        fig, ax = plt.subplots()
        ax.scatter(self.x_datasize, y_acc, color="white")

        # annotate with your emojis
        for i, txt in enumerate(self.emoji_array):
            ax.annotate(txt, (self.x_datasize[i], y_acc[i]),
                        ha="center",
                        va="center",
                        fontsize=30,
                        fontproperties=self.prop if (i != 0 and i != 12) else None)
        ax.set_xlabel('Training Data Size')
        ax.set_ylabel('Test Accuracy')
        ax.set_title(title)
        if savename:
            fig.savefig(savename)
        else:
            plt.show()
    def plot_all(self, alpha_acc):

        fig, ax = plt.subplots(len(alpha_acc), 1)
        index = 0
        for alpha in sorted(alpha_acc.keys()):
            y_acc = alpha_acc[alpha][0]
            ax[index].scatter(self.x_datasize, y_acc, color="white")
            # annotate with your emojis
            for i, txt in enumerate(self.emoji_array):
                ax[index].annotate(txt, (self.x_datasize[i], y_acc[i]),
                            ha="center",
                            va="center",
                            fontsize=10,
                            fontproperties=self.prop if (i != 0 and i != 12) else None)
            ax[index].set_xlabel('Training Data Size')
            ax[index].set_ylabel('Test Accuracy')
            ax[index].set_title(f'alpha={alpha}, acc={"{:.3f}".format(alpha_acc[alpha][1])}')
            index += 1
        fig.savefig('naive_bayes_alphas.png')
        plt.show()