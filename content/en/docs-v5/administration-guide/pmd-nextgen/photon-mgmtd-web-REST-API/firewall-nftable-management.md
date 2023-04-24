---
title:  Firewall nftables Management
weight: 6
---

Use `pmctl` command to manage the firewall nftables. The following section lists the command that you can use to manage the nftables.


## Add nftable ##

To add an nftable, use the following command in `pmctl`:

	pmctl network add-nft-table name <TABLE> family <FAMILY>

Example:
	
	>pmctl network add-nft-table name test99 family inet

## Delete nftable ##

To delete an nftable, use the following command in `pmctl`:

	pmctl network delete-nft-table name <TABLE> family <FAMILY>

Example:

	>pmctl network delete-nft-table name test99 family inet

## Show nftable ##

To show an nftable, use the following command in `pmctl`:

	pmctl network show-nft-table name <TABLE> family <FAMILY>

Example:

	>pmctl network show-nft-table name test99 family inet

## Show all nftables ##

To show all the nftables, use the following command in `pmctl`:

	>pmctl network show-nft-table

## Add nftable chain ##

To add an nftable chain, use the following command in `pmctl`:

	pmctl network add-nft-chain name <CHAIN> table <TABLE> family <FAMILY> hook <HOOK> priority <PRIORITY> type <TYPE> policy <POLICY>

Example:

	>pmctl network add-nft-chain name chain1 table test99 family inet hook input priority 300 type filter policy drop

## Delete nft chain ##

To delete an nftable chain, use the following command in `pmctl`:

	pmctl network delete-nft-chain name <CHAIN> table <TABLE> family <FAMILY>

Example:

	>pmctl network delete-nft-chain name chain1 table test99 family inet

## Show nft chain ##

To show an nftable chain, use the following command in `pmctl`:

	pmctl network show-nft-chain name <CHAIN> table <TABLE> family <FAMILY>

Example:

	>pmctl network show-nft-chain name chain1 table test99 family inet

## Show all nft chain ##

To show all nftable chains, use the following command in `pmctl`:

	>pmctl network show-nft-chain

## Save all nftables ##

To save all nftables, use the following command in `pmctl`:

	>pmctl network nft-save

## Run nft commands ##

To run the nftables command, use the following command in `pmctl`:

	pmctl network nft-run <COMMAND>


Examples:

	>pmctl network nft-run nft add table inet test99


	>pmctl network nft-run nft add chain inet test99 my_chain '{ type filter hook input priority 0; }'


	>pmctl network nft-run nft add rule inet test99 my_chain tcp dport {telnet, http, https} accept


	>pmctl network nft-run nft delete rule inet test99 my_chain handle 3


	>pmctl network nft-run nft delete chain inet test99 my_chain

	
	>pmctl network nft-run nft delete table inet test99

