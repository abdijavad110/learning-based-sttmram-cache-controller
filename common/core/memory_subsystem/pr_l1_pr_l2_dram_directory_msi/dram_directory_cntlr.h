#pragma once

#include "dram_directory_cache.h"
#include "req_queue_list.h"
#include "dram_cntlr.h"
#include "address_home_lookup.h"
#include "shmem_req.h"
#include "shmem_msg.h"
#include "mem_component.h"
#include "memory_manager_base.h"

class NucaCache;

namespace PrL1PrL2DramDirectoryMSI
{
   class DramDirectoryCntlr
   {
      private:
         // Functional Models
         MemoryManagerBase* m_memory_manager;
         AddressHomeLookup* m_dram_controller_home_lookup;
         DramDirectoryCache* m_dram_directory_cache;
         ReqQueueList* m_dram_directory_req_queue_list;

         NucaCache* m_nuca_cache;

         core_id_t m_core_id;
         UInt32 m_cache_block_size;
         UInt32 m_max_hw_sharers;

         ShmemPerfModel* m_shmem_perf_model;

         UInt64 evict_modified, evict_exclusive, evict_shared;

         UInt32 getCacheBlockSize() { return m_cache_block_size; }
         MemoryManagerBase* getMemoryManager() { return m_memory_manager; }
         ShmemPerfModel* getShmemPerfModel() { return m_shmem_perf_model; }

         // Private Functions
         DirectoryEntry* processDirectoryEntryAllocationReq(ShmemReq* shmem_req);
         void processNullifyReq(ShmemReq* shmem_req);

         void processNextReqFromL2Cache(IntPtr address);
         void processExReqFromL2Cache(ShmemReq* shmem_req, Byte* cached_data_buf = NULL);
         void processShReqFromL2Cache(ShmemReq* shmem_req, Byte* cached_data_buf = NULL);
         void retrieveDataAndSendToL2Cache(ShmemMsg::msg_t reply_msg_type, core_id_t receiver, IntPtr address, Byte* cached_data_buf);
         void processDRAMReply(core_id_t sender, ShmemMsg* shmem_msg);

         void processUpgradeReqFromL2Cache(ShmemReq* shmem_req, Byte* cached_data_buf = NULL);

         void processInvRepFromL2Cache(core_id_t sender, ShmemMsg* shmem_msg);
         void processFlushRepFromL2Cache(core_id_t sender, ShmemMsg* shmem_msg);
         void processWbRepFromL2Cache(core_id_t sender, ShmemMsg* shmem_msg);
         void sendDataToNUCA(IntPtr address, core_id_t requester, Byte* data_buf, SubsecondTime now);
         void sendDataToDram(IntPtr address, core_id_t requester, Byte* data_buf, SubsecondTime now);

      public:
         DramDirectoryCntlr(core_id_t core_id,
               MemoryManagerBase* memory_manager,
               AddressHomeLookup* dram_controller_home_lookup,
               NucaCache* nuca_cache,
               UInt32 dram_directory_total_entries,
               UInt32 dram_directory_associativity,
               UInt32 cache_block_size,
               UInt32 dram_directory_max_num_sharers,
               UInt32 dram_directory_max_hw_sharers,
               String dram_directory_type_str,
               SubsecondTime dram_directory_cache_access_time,
               ShmemPerfModel* shmem_perf_model);
         ~DramDirectoryCntlr();

         void handleMsgFromL2Cache(core_id_t sender, ShmemMsg* shmem_msg);
         void handleMsgFromDRAM(core_id_t sender, ShmemMsg* shmem_msg);

         DramDirectoryCache* getDramDirectoryCache() { return m_dram_directory_cache; }
   };

}
