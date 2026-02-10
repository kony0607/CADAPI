//////////////////////////////////////////////////////////////////////////////
//
// Copyright 2026 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software.
//
//////////////////////////////////////////////////////////////////////////////

#pragma once
#include "../../Core/Base.h"
#include "../SimTypeDefs.h"
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef SIMXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_SIM_SIMATTRIBUTEINPUT_CPP__
# define ADSK_SIM_SIMATTRIBUTEINPUT_API XI_EXPORT
# else
# define ADSK_SIM_SIMATTRIBUTEINPUT_API
# endif
#else
# define ADSK_SIM_SIMATTRIBUTEINPUT_API XI_IMPORT
#endif

namespace adsk { namespace sim {

/// !!!!! Warning !!!!!
/// ! This is hidden and not officially supported
/// !!!!! Warning !!!!!
/// 
/// This class defines the methods and properties that pertain to the definition of a simulation attribute.
class SimAttributeInput : public core::Base {
public:

    /// The input entities. The collection can contain vertices, edges, faces, bodies, etc.
    /// All of the entities must be of a single type. For example, it can't contain vertices and faces
    /// but only vertices or faces.
    std::vector<core::Ptr<core::Base>> entities() const;

    ADSK_SIM_SIMATTRIBUTEINPUT_API static const char* classType();
    ADSK_SIM_SIMATTRIBUTEINPUT_API const char* objectType() const override;
    ADSK_SIM_SIMATTRIBUTEINPUT_API void* queryInterface(const char* id) const override;
    ADSK_SIM_SIMATTRIBUTEINPUT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual core::Base** entities_raw(size_t& return_size) const = 0;
    virtual void placeholderSimAttributeInput0() {}
    virtual void placeholderSimAttributeInput1() {}
    virtual void placeholderSimAttributeInput2() {}
    virtual void placeholderSimAttributeInput3() {}
    virtual void placeholderSimAttributeInput4() {}
    virtual void placeholderSimAttributeInput5() {}
    virtual void placeholderSimAttributeInput6() {}
    virtual void placeholderSimAttributeInput7() {}
    virtual void placeholderSimAttributeInput8() {}
    virtual void placeholderSimAttributeInput9() {}
    virtual void placeholderSimAttributeInput10() {}
    virtual void placeholderSimAttributeInput11() {}
    virtual void placeholderSimAttributeInput12() {}
    virtual void placeholderSimAttributeInput13() {}
    virtual void placeholderSimAttributeInput14() {}
};

// Inline wrappers

inline std::vector<core::Ptr<core::Base>> SimAttributeInput::entities() const
{
    std::vector<core::Ptr<core::Base>> res;
    size_t s;

    core::Base** p= entities_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}
}// namespace sim
}// namespace adsk

#undef ADSK_SIM_SIMATTRIBUTEINPUT_API