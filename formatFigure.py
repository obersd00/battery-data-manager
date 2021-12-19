import matplotlib.pyplot as plt



fig = plt.figure()
ax = fig.gca()
#ax.plot(cycnum,spec_caps,'o',c=[0,0,0])
plt.ylabel('Specific Discharge Capacity (mAh / g)',fontname='Arial',fontsize=20,labelpad=10)
plt.yticks(fontname='Arial',fontsize=12)
plt.xlabel('Cycle Number',fontname='Arial',fontsize=20,labelpad=20)
plt.xticks(fontname='Arial',fontsize=12)
x='[insert dataset name]'
plt.title('Cycle life of %s' %x, fontname='Arial',fontsize=20)
plt.legend(['Im a freaking legend'],loc='lower left',bbox_to_anchor=(0,0,0.5,0.5),borderaxespad=0.5,frameon=False)
ax.spines["top"].set_color([0,0,0])
ax.spines["top"].set_linewidth(3)
ax.spines["bottom"].set_linewidth(3)
ax.spines["left"].set_linewidth(3)
ax.spines["right"].set_linewidth(3)
top_ax = ax.secondary_xaxis("top")
top_ax.tick_params(axis='x',direction='in')
top_ax.set_xticklabels([]) #remove number labels from top axis
top_ax.tick_params(length=15,width=2)
ax.tick_params(axis='x',length=15,width=2,direction='in')
ax.tick_params(axis='y',length=10,width=2,direction='in')
plt.show()
