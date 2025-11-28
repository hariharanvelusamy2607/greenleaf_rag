import logging

from rag_pipeline import ingest_markdown

prompt = """# Project Greenleaf

## Real-Time Grand Strategy

—

In a realm divided by races and factions, take command as the Lord of a Faction. 

Be a Conqueror. 

Be a Diplomat. 

Be a Destroyer. 

Guide your empire to be the greatest, through ruthless aggression or diplomatic exchanges, careful forethought or reckless abandon, loyal friendships or shameless betrayals.

The world is your sandbox\!

—

# Campaign (New Game)

**![][image1]**

**Campaign** is the primary mode of playing Project Greenleaf

You (The player) are invited into a new world populated with diverse races, each having their own factions, controlling their own territory. 

Your first steps start with choosing your character and faction in your quest for greatness\!

## Character & Faction Selection

![][image2]

The Character Selection window displays the list of Playable Characters, grouped by their Race.

Each Playable character leads their own faction, belongs to an archetype, and has a list of distinct traits that impact gameplay. They have their own objectives, and they all start at different areas of the world map\!

You inherit the character’s faction, goals, drive and shortcomings\!

# Races

The world of Greenleaf is populated by diverse racial groups.

## Ashenclad

A race of orc-like, war-hungry savages who enjoy the carnage of wars and destruction. Ashenclad has the weakest economy, and they make for poor diplomats, but their strength in numbers is incomparable, and they wrought havoc as easy as they breathe.

## Luminarae

Elven mystics specialized in diplomacy and economy. Luminarae are known to use ranged troops to their full potential, dwindling enemy numbers before they reach their files, and whoever flees gets picked off by their most efficient cavalry.

## Human

The weakest race who have to rely on their technology and science to achieve their goals. Humans do not excel in combat generally, but their wide array of troop types enable the usage of various advanced tactics

# Factions

Factions represent different tribes of the same race that act together.

Factions of the same race tend to share unique gameplay mechanics and units that set them apart from other races.

Each faction has a Lord and their followers, and one or more settlements they control. The factions have a set of goals determined by their Lord that they strive to achieve.

The player will be controlling one such Lord of a faction.

# Overworld Map

The Campaign starts on the Overworld Map, with a view of your default owned capital settlement and your chosen character (**Player Lord**) as an army nearby

![][image3]

## Controls

Camera Movement		W A S D / Mouse Right Click and Drag  
Camera Zoom			Mouse Scroll Up / Down  
Camera Rotate		Q E / Mouse Middle Click and Drag  
Select Character		Left Mouse Click  
Command Character		Right Mouse Click  
Pause Game			P  
Change Game Speed		\+ / \-

## Main HUD

### Top Left HUD

**![][image4]**

1. Portrait of the Player Lord  
2. Player Faction’s resources and their expected change per day  
   1. Gold  
   2. Food  
   3. Industry  
   4. Armaments  
   5. Knowledge

### Top Right HUD

**![][image5]**

1. Diplomacy  
2. Research  
3. Trade  
4. Codex  
5. Council  
6. Current time and Time controls  
7. Settings

### Bottom Right HUD

1. List of Agents in your faction  
2. List of Generals in your faction  
3. List of Provinces held by your faction  
4. List of Current Missions

### Settlement Banner 

1. Owning Faction’s flag  
2. The crown represents if it is the Capital Settlement of its owning faction  
3. Name  
4. Stability  
5. Current Garrison count  
6. Whether its a Major or Minor settlement

The section above the banner represents

1. No of Stationed Agents within the settlement  
2. No of Stationed Generals within the settlement

Hovering over the Banner opens up a section that represents what resources and how many of them are being produced / consumed per day by this settlement

### Character Banner

1. The Character’s faction Flag  
2. The crown represents whether the character is the Lord of its Faction  
3. Character Role:![][image6]General  / ![][image6]Agent  
4. Number of troops accompanying the character  
5. Current Task

# Provinces

The world of Greenleaf is dotted with Provinces.

Provinces are large land areas which the campaign map is divided into. In turn, provinces are divided into local regions called Settlements. Provinces contain up to four settlements.

The UI below displays one such province “Hallowthorn” and its settlements.

![][image7]

Each settlement within a province can be held by different factions, making that province an **incomplete** one, with shared control by the different factions. 

A province in which all settlements are held by the same faction is a **complete** province. 

Complete provinces provide a boost to the economy and stability of the settlements within that province.

A province can be taxed for gold by factions that hold at least one settlement in that province. The **taxation** is only applied to all the settlements in that province that are held by that faction.

You can define the **level of taxation**. High taxation provides more gold, but impacts Stability negatively. No taxation improves stability, at the cost of no tax income.

The **Production** section displays a list of all the resources being produced / consumed in that settlement. Mousing over each resource icon provides more information. **Production Toggle** stops the production of all resources from the province, but improves stability.

The **Stability** is a measure of how happy the populace of a province is, and how likely they are to rebel against the controlling faction. 

Various factors can affect stability, such as buildings, the stationing of armies in the province settlements, taxes, invading armies, etc. Mousing over the Stability bar will tell you all the factors currently affecting the province’s stability.

A province **revolts** if stability drops to \-100, making it a crucial resource to manage


# Settlement

Each province on the campaign map has one major settlement (**Keep**), and usually also from 1-3 minor settlements (**Villages**). There are possibilities for provinces to have only the keep and no villages.

**![][image8]![][image9]**

Clicking on a settlement opens up the Settlement Selection HUD. The HUD displays all the settlements belonging to the province of the selected settlement.

**![][image10]**

**![][image11]**

1. Buildings view  
2. Garrison view  
3. Recruit General (Army)  
4. Recruit Agent

## Buildings View

![][image12]

1. Current Garrison troops count  
2. Deposits available within the Settlement

**Deposits** are crucial resources that determine what buildings can be constructed within that settlement, that extends to what resources can be produced. Each settlement can have at most 3 deposits. The higher the deposits, the more valuable the settlement. Available deposits are **Fish, Fertility, Forest, Stone Deposits, Iron Deposits, Gold Deposits and Coastal**

The **Building Slots** are where you construct buildings within the settlement. Different kinds of settlements have different amounts of building slots. 

1. **Keeps** have a maximum of 8 building slots, 4 of which are locked by default.  
2. **Villages** have a maximum of 4 building slots, 2 of which are locked by default.

![][image13]       ![][image14]

The first slot is always taken up by the settlement building (or ruins) itself. Upgrading the settlement building upgrades the **Settlement Tier**.

Upgrading settlements opens up more building slots, up to its maximum number

The other slots can be used to construct a diverse range of buildings categorised by:

1. Settlement  
2. Resources  
3. Defence  
4. Military Recruitment  
5. Infrastructure  
6. Ancillary  
7. Economy  
8. Military Support  
9. Religion

Each Building provides a different effect to the settlement, the province or the faction. Mouse over each building to know more.

Construction or upgradation of buildings requires you to ensure:

1. The Settlement Tier can accommodate the tier of the building you wish to build  
2. You have enough resources to accommodate the cost of construction

![][image15]    ![][image16]

Each building takes a few days to complete construction. Mouse over on the building under-construction if you wish to cancel. 

Once constructed, clicking on the building will open its **Upgrade Building** menu.

The menu also shows the option to **Demolish** the building at the top.

## Garrison View

Displays the list of garrison troops within each settlement of the selected province.

1. Keeps have 10 Garrison slots  
2. Villages have 6 Garrison slots

All the garrison slots in a settlement are occupied, by default, by the Garrison Militia of the faction. These are very low-quality fodder troops

Certain buildings, on construction, provide better Garrison troops that replace the Garrison Militia as they are provided.

The numbers at the top indicate Total number of Garrison Troops in that settlement, and Total number of units across the entire Garrison

**![][image17]**

## Recruitment (General and Agent)

**![][image18]![][image19]**

Recruitment of Generals and Agents happen from within a settlement. The HUD displays a list of available characters in your faction who can be recruited to the respective roles.

**Supply Lines** represent the total number of Generals and Agents already recruited within the faction. The Cost and Upkeep of all Generals are increased by 10% for each General recruited. The same applies for Agents.

Newly recruited generals and agents spawn immediately near the settlement from where they are recruited.

## Stationed Armies

Armies can be stationed within a settlement of its own faction or an ally faction. Stationed armies support the settlement in battle as reinforcements when the settlement is sieged.

Stationing armies also boost the stability of that settlement.

![][image20]![][image21]

# Characters

Characters are a special type of unit. Characters carry their own attributes and abilities that can benefit or sometimes hinder the faction. The Lord of a faction is a character themselves.

## Roles

The characters by default do not have a physical presence in the campaign map, unless they are recruited to specific roles.

The roles a character can be recruited to:

1. **Generals** are the most powerful and important type. Each army must have a General leading it across the campaign map.

2. **Agents** act as spies or assassins performing actions around the campaign map, but can also join an army and fight in battle.

3. **Governors** act within the confines of a Province. They do not have have a physical presence in the campaign map, but do so in battles when any of the settlements part of their province are being sieged

## Archetype

Each character has a primary and a secondary archetype that defines their skills and tendencies.

### Primary Archetype:

The primary archetype defines their skills and tendencies as a General / Lord

#### Strategist

1. Usually pushovers in diplomacy with the right show of strength  
2. Specialises in **Melee Infantry** and **Ranged Infantry** units  
3. Prefers ambush strategies  
4. Makes for a good Governor

#### Skirmisher

1. Usually pushovers in diplomacy with the right show of strength  
2. Specialises in **Ranged Infantry** and **Cavalry** units  
3. Prefers ambush strategies  
4. Makes for a lousy governor

#### Warlord

1. Prefers chaos. Volatile and more likely to betray diplomatic agreements if it is in their interest  
2. Specialises in **Special** and **Cavalry** units  
3. Prefers outright battles  
4. Makes for a lousy governor

#### Vanquisher

1. Prefers chaos. Volatile and more likely to betray diplomatic agreements if it is in their interest  
2. Specialises in **Melee Infantry** and **Special** units  
3. Prefers outright battles  
4. Makes for a lousy governor

#### Defender

1. Good diplomats. Hard to appease, but makes for a loyal friend  
2. Specialises in **Ranged Infantry** and **Spear** units  
3. Prefers encamping and defensive battles  
4. Makes for a good Governor

#### Vanguard

1. Good diplomats. Hard to appease, but makes for a loyal friend  
2. Specialises solely in **Melee Infantry** units.  
3. Prefers encamping and defensive battles  
4. Makes for a good Governor

### Secondary Archetype:

The secondary archetype defines their skills and tendencies as an Agent.

#### Whisperer

1. Specialised in impacting morale and stability within armies and settlements, and impacting the production and economy of settlements

#### Saboteur

1. Specialised in damaging defences of settlements, inciting riots, blocking army movements

#### Assassin

1. Specialised in dealing damage to armies, characters and garrison troops

## Rank and skills

In the campaign, characters gain experience from battle and various actions, which causes them to gain ranks. When they gain a rank, they can unlock character skills on the skill tree screen.

## Traits

Characters acquire a wide range of character traits as they perform successful actions in the campaign or via story events. These traits have an impact on the character, their governing province, their armies, their skill as an Agent, and their faction itself

##    Attitude and Loyalties

Characters maintain an attitude, between **\-100 and \+100**, with the Lord of their faction (**Loyalty**) and with each other, as colleagues (within the same faction), or otherwise (across factions).

The attitude and loyalties system works as a memory of the characters determining their friends and rivals. Every single action you choose within the campaign map impacts the attitude and loyalties of the characters surrounding you.

**Friendships and rivalries** boost the performance of characters in battle and in the campaign map, as they constantly try to help each other out, or out-perform each other for recognition.

When the **loyalty is low**, the risk of that character **defecting to another faction**, or **rising in rebellion** rises considerably.

A **rival of a character** is much more likely to try and **assassinate** the character. Meanwhile, a character has a chance to **deny any commands** that could negatively affect his **friend**.

Maintaining Attitude and Loyalty within your faction is a crucial step in maintaining a stable empire, and maintaining good attitude with other factions’ Lords ensures lasting peace and diplomacy.

## Recruitment Pool

The recruitment pool of a faction is the list of followers of that faction who can be recruited as a Governor, General or Agent.

Characters can only hold one role, and if they already hold a role, they will have to be disbanded from that role, before being assigned to another role.

Characters join or leave the recruitment pool at a regular interval. 

If a character leaves defects from your faction, they have a chance of being recruited by a rival faction.

## Wounded and Death

Characters can be **wounded or killed** on the campaign map, in battle, via assassinations or via story events, which means they will disappear and be unavailable for several days. 

If a **Lord or General** is wounded, you will have to recruit a follower to **replace** the wounded character. After several days have passed, the wounded characters rejoin the **Recruitment Pool** and can be recruited again at no cost. You do not pay upkeep for wounded characters.

If they are killed, they are permanently removed from your faction.

# Armies (General) and Agents

**![][image22]**

Clicking on a General or an Agent opens the respective HUD.

1. Portrait of the character  
2. Current Health  
3. Food Supplies  
4. Open Character Details Button

## Food Supplies

Armies require **Food Supplies** to function effectively and keep their troops healthy. Food supplies are replenished from the faction’s inventory when the army is stationed within their own faction’s or ally factions’ settlements.

The amount of food supplies needed by an army is determined by the number of troops. Troops consume the food supplies once per day. When the food supply is empty, the army troops attrition. When the food supplies are replenished, the army troops replenish.

## Health \- Attrition and Replenishment

The green bar represents Current Health. Troops attrition or replenish based on food supplies. When a troop has fully attritioned, it is permanently gone from the army.

## Morale \- Daily Upkeep

The yellow bar represents Current Morale. Troops require daily upkeep to function. If the faction does not have enough resources, the troops’ morale reduces gradually. When the morale hits 0, the troop is lost permanently.

## Troops and Recruitment

An army can have a maximum of 10 Troops in addition to the General themselves, making a total of **11 Maximum troops per army.**

Troops can be recruited as long as the Army is within the territory of their own faction’s or Military Access / Ally factions’ settlements.

**Recruiting troops** requires the construction of certain **buildings**. Higher tier buildings provide higher tier troops. Mouse over the buildings to know which troops are unlocked by that building.

Troops take **time to train**. The time **increases incrementally** for each troop set to be trained. While training is in progress, the army cannot be commanded to another action.

![][image23]![][image24]

## Prisoners

After a battle, there is a small chance the generals of the losing army can be captured by the winner. The list of such prisoners are displayed here.

Every day, each prisoner's chance of escaping captivity increases.

You have the option to release prisoners yourself, or execute them. Just know that the faction of the executed prisoner will not take kindly to you.

**![][image25]**

## Character Details HUD

**![][image26]**

Displays the details of the character. Their name, their current Level and experience points, their Lord’s portrait and the loyalty with their Lord.

1. The Character’s stats that governs their effectiveness in battle  
2. List of their acquired Traits  
3. Skill tree  
4. Current Friendships and Rivalries

![][image27]![][image28]![][image29]

## Flag Commands

Commanding an army or an agent to do an action is done via the contextual Flag commands.

The flag commands display a list of applicable commands for the selected character against the intended target.

**![][image30]![][image31]**

**![][image32]![][image33]**

## Army Stances

Armies can be commanded to take up stances. Taking up a new stance takes time to complete, until which the effects of the new stance are not applicable.

1. **Default Stance:**  
   Army can only move in this stance

2. **Encamp Stance:**  
   Focuses on army replenishment  
   Army replenishment \+20%  
   Army food consumption \-100%

3. **Ambush Stance:**  
   Focuses on hiding and ambushing enemy armies. Battles start automatically when an enemy army is near  
   Army is hidden from view  
   Army replenishment \-100%  
   Army food consumption \-20%

4. **Raid Stance:**  
   Focuses on raiding a neutral / enemy settlement  
   Army replenishment \-100%  
   Army food consumption \+20%  
   Army’s faction: Gold \+20 per hour  
   Raided Settlement: Stability \-1 per hour

# Diplomacy

Factions can engage in diplomacy with other factions. The chance of a faction accepting or rejecting a diplomatic treaty is dependent on their attitude towards the proposing faction, how much of a threat the proposer is, and other factors.

The Diplomacy HUD displays the list of factions with whom you can negotiate treaties with.

Once a treaty is proposed, the other faction takes time to reply back. (Marked by a bird symbol) **![][image34]**

Until the reply, you can initiate another diplomatic treaty with that faction.

Cancelling or breaking the rules of a diplomatic treaty has consequences.

**![][image35]![][image36]**

## Send Gift 

Sends a gift of gold to the other faction as Goodwill. Improves the attitude of the faction towards you.

## Trade Agreement 

Trade agreements allow factions to exchange trade resources and generate extra income for both factions.

## Non-Aggression Pact 

Ensures that neither faction in this treaty will declare war on each other.

## Military Access

Allows you to station your armies in and recruit army units from the other faction’s settlements.

## Alliance

The ultimate treaty of friendship, that incorporates both Non-Aggression Pact and Military Access treaty. Factions are expected to join wars against the enemies of their allies

## Subjugation

Subjugated factions are expected to send a daily tribute to their Subjugator. You can also directly control the armies and agents of your subjugated factions as if they are your own.

## War

Declaring war on any faction will break all ongoing treaties with that faction. When war is declared against a faction, the allies of both sides also jump in

## Truce

Declaration to stop the ongoing war. Truce is typically not accepted until the war has dragged on for a long time, or someone is gaining the upper hand in the war.

# Trade

The Trade window lists down all the factions that are currently in any of the below treaties with your faction:

1. Your Subjugator  
2. Factions you have subjugated  
3. Trade agreement  
4. Alliance

You can set the number of resources you want to import or export per day from these factions here. 

Continuously failing to provide the resources set in the trade window to the respective faction will anger them and cause them to break their treaty. 

Setting the resources to 0 in import / export for a while will also cause them to break the treaty because of the treaty being non-profitable.

# Research Tree

**![][image37]**

Unlocking research in the Research Tree provides faction-wide buffs.

The research tree is an open system with multiple groups categorized by Military, Production, Defence tech trees. The tech trees each contain multiple groups. Each group is categorized by one major research and 4 minor researches. 

You are free to research tech in any order you want by spending the Knowledge resource from your faction’s inventory. Unlocked research is non-refundable."
"""
if __name__ == "__main__":
    chunk_ids = ingest_markdown(prompt)
    logging.info("Successfully ingested %d chunk(s)", len(chunk_ids))