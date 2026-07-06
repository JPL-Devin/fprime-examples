// ======================================================================
// \title  Producer.hpp
// \author mstarch
// \brief  hpp file for Producer component implementation class
// ======================================================================

#ifndef DataProduct_Producer_HPP
#define DataProduct_Producer_HPP

#include "DataProduct/Producer/ProducerComponentAc.hpp"

#include "config/ProcTypeEnumAc.hpp"

namespace DataProduct {

class Producer final : public ProducerComponentBase {
  public:
    constexpr static const FwSizeType RECORD_COUNT = 100;  //!< Number of records of each type in the data product
    // ----------------------------------------------------------------------
    // Component construction and destruction
    // ----------------------------------------------------------------------

    //! Construct Producer object
    Producer(const char* const compName  //!< The component name
    );

    //! Destroy Producer object
    ~Producer();

  private:
    // ----------------------------------------------------------------------
    // Handler implementations for typed input ports
    // ----------------------------------------------------------------------

    //! Handler implementation for run
    //!
    //! Schedule input port
    void run_handler(FwIndexType portNum,  //!< The port number
                     U32 context           //!< The call order
                     ) override;

  private:
    // ----------------------------------------------------------------------
    // Handler implementations for commands
    // ----------------------------------------------------------------------

    //! Handler implementation for command SET_PROC_TYPES
    //!
    //! Command to set the processing types applied to future data product containers
    void SET_PROC_TYPES_cmdHandler(FwOpcodeType opCode,           //!< The opcode
                                   U32 cmdSeq,                    //!< The command sequence number
                                   Fw::DpCfg::ProcType procTypes  //!< The processing types
                                   ) override;

  private:
    FwSizeType m_count;               //!< Count of serialized records
    DpContainer m_container;          //!< Data product container (currently allocated)
    bool m_containerValid;            //!< Whether the container is valid
    Fw::DpCfg::ProcType m_procTypes;  //!< Processing types applied to data product containers
};

}  // namespace DataProduct

#endif
